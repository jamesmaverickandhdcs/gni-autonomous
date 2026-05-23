export default function ResetBanner() {
  return (
    <div className="w-full bg-blue-950 border-b border-blue-800 text-blue-100 px-4 py-3 text-sm">
      <div className="max-w-5xl mx-auto flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-3">
        <span className="font-semibold text-blue-300 whitespace-nowrap">
          🕊️ PHI-003 Freedom from Fear — Now Live
        </span>
        <span className="text-blue-200">
          GNI Autonomous now runs under the PHI-003 Freedom from Fear standard.
          Every report answers three questions: what is happening, what honest analysis says, and what you can do.
          Intelligence for every human being — from teenagers to senior citizens — without manipulation and without fear amplification.{" "}
          <span className="text-blue-300 font-medium">Free. Always on. No login needed.</span>
        </span>
      </div>
    </div>
  );
}
