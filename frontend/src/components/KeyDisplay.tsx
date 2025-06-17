"use client";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import AnimatedBackground from "@/components/AnimatedBackground";
import { motion } from "framer-motion";
import { Save } from "lucide-react";

export default function KeyDisplay({
  keys,
  onConfirm,
}: {
  keys: {
    mnemonic: string;
    dilithium_pub: string;
    kyber_pub: string;
    user_id: string;
  };
  onConfirm: () => void;
}) {
  const mnemonicWords = keys.mnemonic.split(" ");

  return (
    <div className="relative flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 p-4 overflow-hidden">
      <AnimatedBackground />

      {/* Removed the initial, animate, and transition props for the main card pop animation */}
      {/* The `relative z-10 w-full max-w-md mx-auto` className is kept for layout */}
      <div className="relative z-10 w-full max-w-md mx-auto">
        <Card className="relative p-8 text-center bg-white/10 backdrop-blur-xl border border-white/20 shadow-2xl">
          {/* Decorative elements - kept for consistent style */}
          <div className="absolute -top-2 -left-2 w-4 h-4 bg-blue-500 rounded-full animate-pulse" />
          <div className="absolute -top-2 -right-2 w-4 h-4 bg-purple-500 rounded-full animate-pulse delay-300" />
          <div className="absolute -bottom-2 -left-2 w-4 h-4 bg-green-500 rounded-full animate-pulse delay-700" />
          <div className="absolute -bottom-2 -right-2 w-4 h-4 bg-pink-500 rounded-full animate-pulse delay-1000" />

          {/* This motion.div still controls the fade-in of the content inside the card */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.3 }} // Slightly reduced delay since the card itself doesn't animate in
          >
            <h2 className="text-2xl font-bold text-white mb-6 text-center leading-relaxed">
              You have successfully registered to the blockchain!
            </h2>

            {/* User Address Display */}
            <div className="mb-6 bg-white/5 rounded-lg p-4 border border-white/10">
              <p className="text-sm text-slate-400 mb-2 font-medium">
                Your User ID:
              </p>
              <div className="p-3 bg-slate-800 rounded-md break-all text-sm font-mono text-blue-300 select-all cursor-text">
                {keys.user_id}
              </div>
            </div>

            <p className="text-md text-slate-300 mb-6 text-center max-w-sm mx-auto">
              Please save these values as you'll only see them once.
            </p>

            {/* Mnemonic Display */}
            <div className="mb-8 bg-white/5 rounded-lg p-4 border border-white/10">
              <p className="text-sm text-slate-400 mb-3 font-medium">
                Mnemonic Phrase:
              </p>
              <div className="flex flex-wrap gap-2 justify-center">
                {mnemonicWords.map((word, index) => (
                  <motion.span
                    key={index}
                    className="px-3 py-1 bg-blue-600/20 text-blue-300 rounded-full text-xs font-semibold shadow-sm backdrop-blur-sm border border-blue-600/30"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3, delay: 0.5 + index * 0.05 }} // Adjusted delay for word pop-in
                  >
                    {word}
                  </motion.span>
                ))}
              </div>
            </div>

            <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
              <Button
                onClick={onConfirm}
                className="w-full h-12 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 border-0 flex items-center justify-center space-x-2"
              >
                <Save className="w-5 h-5" />
                <span>I have saved my keys</span>
              </Button>
            </motion.div>
          </motion.div>
        </Card>
      </div>
    </div>
  );
}
