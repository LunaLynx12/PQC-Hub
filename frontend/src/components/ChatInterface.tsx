import { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";
import ContactsSidebar from "@/components/ContactsSidebar";
import ChatArea from "@/components/ChatArea";
import AnimatedBackground from "@/components/AnimatedBackground";

interface Participant {
  id: number;
  name: string;
  avatar?: string;
  status?: "online" | "offline" | "away";
}

interface Message {
  id: number;
  senderId: number;
  text: string;
  timestamp: string;
  status?: "sent" | "delivered" | "read";
}

interface Conversation {
  id: number;
  name: string;
  isGroup: boolean;
  participants: Participant[];
  messages: Message[];
  lastMessage?: string;
  unreadCount?: number;
  lastSeen?: string;
}

export default function App() {
  const [participants, setParticipants] = useState<Participant[]>([]);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedConversationId, setSelectedConversationId] =
    useState<number>(1);
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8001/ws/chain");
    socketRef.current = socket;

    socket.onopen = () => {
      console.log("WebSocket connected");
      // You can send a message here if your server expects a handshake
      // socket.send(JSON.stringify({ type: "get_users" }));
    };

    socket.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        console.log(message)
        if (message.type === "users_list") {
          setParticipants(message.data);
          // Optional: dynamically generate 1-on-1 conversations
          const generatedConversations: Conversation[] = message.data.map(
            (user: Participant) => ({
              id: user.id,
              name: user.name,
              isGroup: false,
              participants: [user],
              messages: [],
              lastMessage: "No messages yet",
              lastSeen: "Just now",
            })
          );
          setConversations(generatedConversations);
        }
      } catch (err) {
        console.error("Failed to parse WebSocket message", err);
      }
    };

    socket.onclose = () => {
      console.log("WebSocket disconnected");
    };

    return () => {
      socket.close();
    };
  }, []);

  const selectedConversation = conversations.find(
    (c) => c.id === selectedConversationId
  );

  function handleSendMessage(message: string) {
    console.log(
      `Send message "${message}" to conversation ID ${selectedConversationId}`
    );
  }

  return (
    <div className="relative flex h-screen w-full bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 overflow-hidden">
      <AnimatedBackground />
      <motion.div
        initial={{ scale: 0.95, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        className="relative z-10 flex w-full h-full bg-white/10 backdrop-blur-xl border border-white/20 shadow-2xl"
      >
        <div className="absolute -top-1 -left-1 w-3 h-3 bg-blue-500 rounded-full animate-pulse" />
        <div className="absolute -top-1 -right-1 w-3 h-3 bg-purple-500 rounded-full animate-pulse delay-300" />
        <div className="absolute -bottom-1 -left-1 w-3 h-3 bg-green-500 rounded-full animate-pulse delay-700" />
        <div className="absolute -bottom-1 -right-1 w-3 h-3 bg-pink-500 rounded-full animate-pulse delay-1000" />

        {/* Sidebar */}
        <div className="w-80 flex-shrink-0 h-full">
          <ContactsSidebar
            conversations={conversations}
            selectedConversationId={selectedConversationId}
            onSelectConversation={setSelectedConversationId}
          />
        </div>

        {/* Chat Area */}
        <div className="flex-1 h-full">
          {selectedConversation ? (
            <ChatArea
              conversation={selectedConversation}
              participants={participants}
              onSendMessage={handleSendMessage}
            />
          ) : (
            <div className="text-white p-8">No conversation selected.</div>
          )}
        </div>
      </motion.div>
    </div>
  );
}
