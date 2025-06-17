"use client";
import { Card } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";

export default function KeyDisplay({
  keys,
  onConfirm,
}: {
  keys: { pub: string; priv: string };
  onConfirm: () => void;
}) {
  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-br from-slate-100 to-white p-4">
      <Card className="p-6 max-w-md w-full shadow-lg">
        <h2 className="text-xl font-semibold text-slate-800 mb-4 text-center">
          Your Keys
        </h2>
        <div className="mb-4">
          <p className="text-sm text-slate-600 mb-1">Private Key1:</p>
          <pre className="bg-slate-100 p-2 rounded text-xs break-all">
            {keys.pub}
          </pre>
        </div>
        <div>
          <p className="text-sm text-slate-600 mb-1">Private Key2:</p>
          <pre className="bg-red-100 p-2 rounded text-xs break-all text-red-600">
            {keys.priv}
          </pre>
        </div>
        <Separator className="my-4" />
        <button
          onClick={onConfirm}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded"
        >
          I have saved my keys
        </button>
      </Card>
    </div>
  );
}
