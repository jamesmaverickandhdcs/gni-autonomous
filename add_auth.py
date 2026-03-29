import os
import re

routes_dir = "src/app/api"

# Routes that should NOT be protected (internal use only)
SKIP_ROUTES = [
    "mission-control",
    "mission-control-history",
]

# Find all route.ts files
route_files = []
for root, dirs, files in os.walk(routes_dir):
    for file in files:
        if file == "route.ts":
            route_files.append(os.path.join(root, file))

print(f"Found {len(route_files)} route files")

fixed = 0
skipped = 0
already = 0

for filepath in sorted(route_files):
    # Check if should skip
    skip = False
    for s in SKIP_ROUTES:
        if s in filepath.replace("\\", "/"):
            skip = True
            break
    if skip:
        print(f"SKIP: {filepath}")
        skipped += 1
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Already has validation
    if "validateApiKey" in content:
        print(f"ALREADY: {filepath}")
        already += 1
        continue

    # Add import after first line (export const dynamic or import)
    # Find the first GET/POST function
    if "export async function GET" not in content and "export async function POST" not in content:
        print(f"NO_HANDLER: {filepath}")
        skipped += 1
        continue

    # Add import at top (after 'use server' or after first import)
    if "import { validateApiKey }" not in content:
        # Add after the last existing import line
        lines = content.split("\n")
        last_import_idx = 0
        for i, line in enumerate(lines):
            if line.startswith("import "):
                last_import_idx = i
        
        lines.insert(last_import_idx + 1, "import { validateApiKey } from '@/lib/auth'")
        content = "\n".join(lines)

    # Add validation check inside GET function
    # Pattern: export async function GET(request: NextRequest) {\n
    def add_validation(match):
        func_sig = match.group(0)
        return func_sig + "\n  const authError = validateApiKey(request)\n  if (authError) return authError\n"

    # Handle GET with NextRequest
    content = re.sub(
        r'export async function GET\(request: NextRequest\) \{\n',
        add_validation,
        content
    )

    # Handle GET with request: Request
    content = re.sub(
        r'export async function GET\(request: Request\) \{\n',
        lambda m: m.group(0) + "\n  const authError = validateApiKey(request as any)\n  if (authError) return authError\n",
        content
    )

    # Handle GET() with no params -- add request param
    content = re.sub(
        r'export async function GET\(\) \{\n',
        lambda m: "export async function GET(request: NextRequest) {\n  const authError = validateApiKey(request)\n  if (authError) return authError\n",
        content
    )

    # Handle POST
    content = re.sub(
        r'export async function POST\(request: NextRequest\) \{\n',
        add_validation,
        content
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"FIXED: {filepath}")
    fixed += 1

print(f"\nSummary: {fixed} fixed | {skipped} skipped | {already} already done")