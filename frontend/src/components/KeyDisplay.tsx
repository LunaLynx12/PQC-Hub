"use client";
import { Card } from "@/components/ui/card";

export default function KeyDisplay({
  keys,
  onConfirm,
}: {
  keys: { mnemonic: string; dilithium_pub: string; kyber_pub: string; user_id: string};
  onConfirm: () => void;
}) {
  // Split mnemonic into words
  const mnemonicWords = keys.mnemonic.split(" ");

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-br from-slate-100 to-white p-4">
      <Card className="p-6 max-w-md w-full shadow-lg rounded-xl border border-slate-200 bg-white/95 backdrop-blur-sm">
        <h2 className="text-xl font-semibold text-slate-800 mb-4 text-center">
          You have successfully registered to the blockchain. Please save these values as you'll only see them once!
        </h2>

        {/* User Address Display */}
        <div className="mb-6">
          <p className="text-sm text-slate-600 mb-1">Your User ID:</p>
          <div className="p-3 bg-slate-100 rounded-lg break-all text-sm font-mono text-slate-800 mb-4">
            {keys.user_id}
          </div>
        </div>

        {/* Mnemonic Display */}
        <div className="mb-6">
          <p className="text-sm text-slate-600 mb-3">Mnemonic:</p>
          <div className="flex flex-wrap gap-2 justify-center">
            {mnemonicWords.map((word, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-slate-100 rounded-full text-xs text-slate-800 shadow-sm hover:bg-slate-200 transition-all duration-200"
              >
                {word}
              </span>
            ))}
          </div>
        </div>

        <button
          onClick={onConfirm}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded transition-colors duration-200"
        >
          I have saved my keys
        </button>
      </Card>
    </div>
  );
}