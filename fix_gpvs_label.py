f = open("src/app/page.tsx", "r", encoding="utf-8")
c = f.read()
f.close()

old = "Powered by GPVS v1.0"
new = "Powered by GPVS v1.1"

c = c.replace(old, new)

f = open("src/app/page.tsx", "w", encoding="utf-8")
f.write(c)
f.close()
print("Done")