"use client";
import { useEffect, useState } from "react";
import RegisterScreen from "@/components/RegisterScreen";
import KeyDisplay from "@/components/KeyDisplay";
import App from "@/components/ChatInterface";

export default function Page() {
  const [keys, setKeys] = useState<{ pub: string; priv: string } | null>(null);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    const pub = localStorage.getItem("pub");
    const priv = localStorage.getItem("priv");
    if (pub && priv) {
      setKeys({ pub, priv });
      setSaved(true);
    }
  }, []);

  const handleRegistered = (generatedKeys: { pub: string; priv: string }) => {
    setKeys(generatedKeys);
  };

  const handleConfirm = () => {
    if (keys) {
      localStorage.setItem("pub", keys.pub);
      localStorage.setItem("priv", keys.priv);
      setSaved(true);
    }
  };

  if (!keys) return <RegisterScreen onRegistered={handleRegistered} />;
  if (keys && !saved)
    return <KeyDisplay keys={keys} onConfirm={handleConfirm} />;
  return <App />;
}
