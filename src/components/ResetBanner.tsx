export default function ResetBanner() {
  return (
    <div className="w-full bg-blue-950 border-b border-blue-800 text-blue-100 px-4 py-3 text-sm">
      <div className="max-w-5xl mx-auto flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-3">
        <span className="font-semibold text-blue-300 whitespace-nowrap">
          🔄 GNI is Rebuilding
        </span>
        <span className="text-blue-200">
          GNI Autonomous is transitioning to a new foundation — the PHI-003 Freedom from Fear standard.
          Every reader, from teenagers to senior citizens, will be able to clearly understand what
          threatens their freedom, without manipulation and without fear amplification.
          Historical reports are being reset. New intelligence begins shortly.{" "}
          <span className="text-blue-300 font-medium">The system continues running.</span>
        </span>
      </div>
    </div>
  );
}
