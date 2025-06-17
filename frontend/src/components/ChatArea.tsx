import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  Send,
  Users,
  MoreVertical,
  Phone,
  Video,
  Smile,
  Paperclip,
} from "lucide-react";
import { motion } from "framer-motion";

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

interface ChatAreaProps {
  conversation: Conversation;
  participants: Participant[];
  onSendMessage: (message: string) => void;
}

export default function ChatArea({
  conversation,
  participants,
  onSendMessage,
}: ChatAreaProps) {
  const [input, setInput] = useState("");

  function handleSend() {
    if (!input.trim()) return;
    onSendMessage(input);
    setInput("");
  }

  const messageVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 },
  };

  return (
    <div className="flex flex-col h-full bg-black/20">
      {/* Chat Header */}
      <div className="flex-shrink-0 bg-white/5 p-4 border-b border-white/10 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <Avatar className="w-10 h-10">
            {conversation.isGroup ? (
              <AvatarFallback className="bg-gradient-to-br from-blue-500 to-purple-600 text-white">
                <Users className="h-5 w-5" />
              </AvatarFallback>
            ) : (
              <AvatarImage
                src={conversation.participants[0]?.avatar}
                alt={conversation.participants[0]?.name}
              />
            )}
          </Avatar>

          <div>
            <h2 className="font-semibold text-white">{conversation.name}</h2>
            <p className="text-sm text-slate-400">
              {conversation.isGroup
                ? `${conversation.participants.length} members`
                : conversation.participants[0]?.status || "offline"}
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <Button
            variant="ghost"
            size="icon"
            className="text-slate-400 hover:text-white"
          >
            <Phone className="h-5 w-5" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            className="text-slate-400 hover:text-white"
          >
            <Video className="h-5 w-5" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            className="text-slate-400 hover:text-white"
          >
            <MoreVertical className="h-5 w-5" />
          </Button>
        </div>
      </div>

      {/* Messages Area */}
      <ScrollArea className="flex-1 p-6">
        <div className="space-y-6">
          {conversation.messages.map((msg, index) => {
            const sender = participants.find((p) => p.id === msg.senderId);
            const isMe = sender?.id === 1;
            const showAvatar =
              !isMe &&
              (index === 0 ||
                conversation.messages[index - 1]?.senderId !== msg.senderId);

            return (
              <motion.div
                key={msg.id}
                initial="hidden"
                animate="visible"
                variants={messageVariants}
                transition={{ duration: 0.3, delay: 0.1 * index }}
                className={`flex ${isMe ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`flex max-w-xs lg:max-w-md ${
                    isMe ? "flex-row-reverse" : "flex-row"
                  } items-end space-x-2`}
                >
                  {showAvatar && !isMe && (
                    <Avatar className="w-8 h-8">
                      <AvatarImage src={sender?.avatar} alt={sender?.name} />
                      <AvatarFallback>{sender?.name?.[0]}</AvatarFallback>
                    </Avatar>
                  )}

                  <div className={`${showAvatar && !isMe ? "" : "ml-10"}`}>
                    {!isMe && conversation.isGroup && showAvatar && (
                      <p className="text-xs text-slate-400 mb-1 ml-3">
                        {sender?.name}
                      </p>
                    )}

                    <div
                      className={`px-4 py-3 rounded-2xl shadow-sm ${
                        isMe
                          ? "bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-br-md"
                          : "bg-white/10 text-white rounded-bl-md border border-white/10"
                      }`}
                    >
                      <p className="text-sm leading-relaxed">{msg.text}</p>
                    </div>

                    <div
                      className={`flex items-center mt-1 space-x-1 ${
                        isMe ? "justify-end" : "justify-start"
                      }`}
                    >
                      <span className="text-xs text-slate-400">
                        {msg.timestamp}
                      </span>
                      {isMe && msg.status && (
                        <div
                          className={`w-2 h-2 rounded-full ${
                            msg.status === "read"
                              ? "bg-blue-500"
                              : msg.status === "delivered"
                              ? "bg-slate-400"
                              : "bg-slate-500"
                          }`}
                        />
                      )}
                    </div>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </ScrollArea>

      {/* Message Input */}
      <div className="flex-shrink-0 bg-white/5 p-4 border-t border-white/10">
        <div className="flex items-end space-x-3">
          <Button
            variant="ghost"
            size="icon"
            className="text-slate-400 hover:text-white mb-2"
          >
            <Paperclip className="h-5 w-5" />
          </Button>

          <div className="flex-1 relative">
            <Input
              type="text"
              placeholder={`Message ${conversation.name}...`}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              className="pr-12 py-3 bg-white/5 border-white/10 text-white placeholder:text-slate-400 focus:bg-black/10 focus:border-blue-500 transition-colors"
            />
            <Button
              variant="ghost"
              size="icon"
              className="absolute right-2 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-white"
            >
              <Smile className="h-4 w-4" />
            </Button>
          </div>

          <Button
            onClick={handleSend}
            disabled={!input.trim()}
            size="icon"
            className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-full shadow-lg transition-all duration-300 hover:shadow-xl"
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}
