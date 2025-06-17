"use client";
import { useEffect, useState } from "react";
import RegisterScreen from "@/components/RegisterScreen";
import KeyDisplay from "@/components/KeyDisplay";
import App from "@/components/ChatInterface";

export default function Page() {
  const [keys, setKeys] = useState<{ dilithium_pub: string; kyber_pub: string } | null>(null);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    const dilithium_pub = localStorage.getItem("dilithium_pub");
    const kyber_pub = localStorage.getItem("kyber_pub");
    if (dilithium_pub && kyber_pub) {
      setKeys({ dilithium_pub, kyber_pub });
      setSaved(true);
    }
  }, []);

  const handleRegistered = (generatedKeys: { dilithium_pub: string; kyber_pub: string }) => {
    setKeys(generatedKeys);
  };

  const handleConfirm = () => {
    if (keys) {
      localStorage.setItem("dilithium_pub", keys.dilithium_pub);
      localStorage.setItem("kyber_pub", keys.kyber_pub);
      setSaved(true);
    }
  };

  if (!keys) return <RegisterScreen onRegistered={handleRegistered} />;
  if (keys && !saved)
    return <KeyDisplay keys={keys} onConfirm={handleConfirm} />;
  return <App />;
}
