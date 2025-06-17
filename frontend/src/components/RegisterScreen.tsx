import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { motion } from "framer-motion";
import { Shield, Lock, Globe, Zap } from "lucide-react";
import AnimatedBackground from "@/components/AnimatedBackground";

export default function RegisterScreen({
  onRegistered,
}: {
  onRegistered: (keys: { mnemonic: string; dilithium_pub: string; kyber_pub: string; user_id: string}) => void;
}) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleRegister = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch("http://127.0.0.1:8000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({}), // Add empty object
      });

      if (!res.ok) throw new Error("Failed to register");

      const data = await res.json();
      console.log("Full response from backend:", data); // 🔍 Add this line to see full response

      onRegistered({
        mnemonic: data.mnemonic || "N/A",
        dilithium_pub: data.dilithium_priv || "N/A",  // Or adjust as needed
        kyber_pub: data.kyber_pub || "N/A",    // Or adjust as needed
        user_id: data.user_id || "N/A"
      });
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const features = [
    {
      icon: Shield,
      title: "Quantum-Safe",
      description: "Post-quantum cryptography",
    },
    {
      icon: Globe,
      title: "Decentralized",
      description: "No central authority",
    },
    {
      icon: Lock,
      title: "Private",
      description: "Zero data collection",
    },
    {
      icon: Zap,
      title: "Instant",
      description: "Real-time messaging",
    },
  ];

  return (
    <div className="relative flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 p-4 overflow-hidden">
      <AnimatedBackground />

      <div className="relative z-10 w-full max-w-4xl mx-auto">
        {/* Header */}
        <motion.div
          className="text-center mb-12"
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        >
          <motion.h1
            className="text-6xl md:text-7xl font-bold bg-gradient-to-r from-blue-400 via-purple-500 to-blue-600 bg-clip-text text-transparent mb-6"
            initial={{ scale: 0.5 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            PQC Hub
          </motion.h1>

          <motion.p
            className="text-xl text-slate-300 max-w-2xl mx-auto leading-relaxed"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            The future of secure communication is here. Experience
            quantum-resistant messaging with complete privacy and
            decentralization.
          </motion.p>
        </motion.div>

        {/* Features Grid */}
        <motion.div
          className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-12"
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
        >
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              className="text-center"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.8 + index * 0.1 }}
              whileHover={{ scale: 1.05 }}
            >
              <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-blue-500/20 to-purple-600/20 rounded-2xl flex items-center justify-center backdrop-blur-sm border border-blue-500/20">
                <feature.icon className="w-8 h-8 text-blue-400" />
              </div>
              <h3 className="text-white font-semibold mb-2">{feature.title}</h3>
              <p className="text-slate-400 text-sm">{feature.description}</p>
            </motion.div>
          ))}
        </motion.div>

        {/* Main Card */}
        <motion.div
          initial={{ scale: 0, rotateY: 180 }}
          animate={{ scale: 1, rotateY: 0 }}
          transition={{
            duration: 0.8,
            delay: 1.2,
            type: "spring",
            stiffness: 100,
          }}
          className="w-full max-w-md mx-auto"
        >
          <Card className="relative p-8 text-center bg-white/10 backdrop-blur-xl border border-white/20 shadow-2xl">
            {/* Decorative elements */}
            <div className="absolute -top-2 -left-2 w-4 h-4 bg-blue-500 rounded-full animate-pulse" />
            <div className="absolute -top-2 -right-2 w-4 h-4 bg-purple-500 rounded-full animate-pulse delay-300" />
            <div className="absolute -bottom-2 -left-2 w-4 h-4 bg-green-500 rounded-full animate-pulse delay-700" />
            <div className="absolute -bottom-2 -right-2 w-4 h-4 bg-pink-500 rounded-full animate-pulse delay-1000" />

            {/* Content */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.8, delay: 1.5 }}
            >
              <motion.div
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <Button
                  onClick={handleRegister}
                  disabled={loading}
                  className="w-full h-12 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 border-0"
                >
                  {loading ? (
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{
                        duration: 1,
                        repeat: Infinity,
                        ease: "linear",
                      }}
                      className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full"
                    />
                  ) : (
                    <span className="flex items-center space-x-2">
                      <Zap className="w-5 h-5" />
                      <span>Register</span>
                    </span>
                  )}
                </Button>
              </motion.div>

              {error && (
                <motion.p
                  className="text-sm text-red-400 mt-4 p-3 bg-red-500/10 rounded-lg border border-red-500/20"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  {error}
                </motion.p>
              )}
            </motion.div>
          </Card>
        </motion.div>

        {/* Footer */}
        <motion.div
          className="text-center mt-12"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 2.5 }}
        >
          <p className="text-slate-400 text-sm">
            Powered by post-quantum cryptography • Built for the future
          </p>
        </motion.div>
      </div>
    </div>
  );
}
