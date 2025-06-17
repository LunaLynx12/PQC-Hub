"use client";

import { motion } from "framer-motion";
import { useEffect, useState } from "react";

interface Orb {
  width: number;
  height: number;
  left: string;
  top: string;
}

const generateOrbs = (count: number): Orb[] => {
  return Array.from({ length: count }).map(() => ({
    width: Math.random() * 200 + 150, // 150–350 px
    height: Math.random() * 200 + 100, // 100–300 px
    left: `${Math.random() * 100}%`,
    top: `${Math.random() * 100}%`,
  }));
};

export default function AnimatedBackground() {
  const [orbs, setOrbs] = useState<Orb[] | null>(null);

  useEffect(() => {
    // Only run on client
    setOrbs(generateOrbs(6));
  }, []);

  if (!orbs) return null; // Don't render on server

  return (
    <>
      {orbs.map((orb, i) => (
        <motion.div
          key={i}
          className="absolute rounded-full bg-gradient-to-r from-blue-400/20 to-purple-600/20 blur-xl"
          style={{
            width: orb.width,
            height: orb.height,
            left: orb.left,
            top: orb.top,
          }}
          animate={{
            x: [0, 20, -20, 0],
            y: [0, -20, 20, 0],
          }}
          transition={{
            duration: 10,
            repeat: Infinity,
            repeatType: "loop",
            ease: "easeInOut",
          }}
        />
      ))}
    </>
  );
}
