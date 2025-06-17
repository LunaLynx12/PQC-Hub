import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { Search, Users, Clipboard, User, Check } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";

interface Participant {
  id: number;
  name: string;
  avatar?: string;
  status?: "online" | "offline" | "away";
}

interface Conversation {
  id: number;
  name: string;
  isGroup: boolean;
  participants: Participant[];
  messages: any[];
  lastMessage?: string;
  unreadCount?: number;
  lastSeen?: string;
}

interface ContactsSidebarProps {
  conversations: Conversation[];
  selectedConversationId: number;
  onSelectConversation: (id: number) => void;
}

export default function ContactsSidebar({
  conversations,
  selectedConversationId,
  onSelectConversation,
}: ContactsSidebarProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const [userAddress, setUserAddress] = useState("");
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const storedId = localStorage.getItem("user_id");
    if (storedId) setUserAddress(storedId);
  }, []);

  const filteredConversations = conversations.filter((convo) =>
    convo.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  function getStatusColor(status?: string) {
    switch (status) {
      case "online":
        return "bg-green-500";
      case "away":
        return "bg-yellow-500";
      case "offline":
        return "bg-gray-400";
      default:
        return "bg-gray-400";
    }
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(userAddress);
    setCopied(true);
    setTimeout(() => setCopied(false), 1000);
  };

  return (
    <div className="flex flex-col h-full bg-white/5 border-r border-white/10">
      {/* Header */}
      <div className="flex-shrink-0 p-6 border-b border-white/10">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            PQC Chat
          </h1>

          {/* User Icon with Popover */}
          <Popover>
            <PopoverTrigger asChild>
              <Button
                variant="ghost"
                size="icon"
                className="text-slate-400 hover:text-white"
              >
                <User className="h-5 w-5" />
              </Button>
            </PopoverTrigger>
            <PopoverContent
              className="bg-white/5 border border-white/10 shadow-lg backdrop-blur-md text-white p-3 rounded-xl w-fit"
              side="bottom"
              align="end"
            >
              <div className="flex items-center space-x-2">
                <span className="text-sm font-mono truncate max-w-[120px]">
                  {userAddress}
                </span>
                <motion.button
                  onClick={handleCopy}
                  whileTap={{ scale: 0.85 }}
                  className="text-white hover:text-blue-400 transition-colors"
                >
                  {copied ? (
                    <Check className="w-4 h-4 text-green-400" />
                  ) : (
                    <Clipboard className="w-4 h-4" />
                  )}
                </motion.button>
              </div>
            </PopoverContent>
          </Popover>
        </div>

        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-500 h-4 w-4" />
          <Input
            placeholder="Search conversations..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 bg-white/5 border-white/10 text-white placeholder:text-slate-400 focus:bg-black/10 focus:border-blue-500 transition-colors"
          />
        </div>
      </div>

      {/* Conversations List */}
      <ScrollArea className="flex-1">
        <div className="p-2">
          {filteredConversations.map((convo, index) => {
            const isSelected = convo.id === selectedConversationId;
            const mainParticipant = convo.isGroup
              ? null
              : convo.participants[0];

            return (
              <motion.div
                key={convo.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: 0.4 + index * 0.05 }}
                whileHover={{
                  scale: 1.02,
                  backgroundColor: "rgba(255, 255, 255, 0.08)",
                }}
                whileTap={{ scale: 0.98 }}
              >
                <Card
                  onClick={() => onSelectConversation(convo.id)}
                  className={`mb-2 p-4 cursor-pointer transition-all duration-200 shadow-sm ${
                    isSelected
                      ? "bg-blue-600/20 border-blue-500/50"
                      : "bg-white/5 border-white/10 hover:bg-white/10"
                  }`}
                >
                  <div className="flex items-start space-x-3">
                    <div className="relative">
                      <Avatar className="w-12 h-12">
                        {convo.isGroup ? (
                          <AvatarFallback className="bg-gradient-to-br from-blue-500 to-purple-600 text-white font-semibold">
                            <Users className="h-5 w-5" />
                          </AvatarFallback>
                        ) : (
                          <AvatarImage
                            src={mainParticipant?.avatar}
                            alt={mainParticipant?.name}
                          />
                        )}
                      </Avatar>
                      {!convo.isGroup && mainParticipant?.status && (
                        <div
                          className={`absolute -bottom-1 -right-1 w-4 h-4 rounded-full border-2 border-white ${getStatusColor(
                            mainParticipant.status
                          )}`}
                        />
                      )}
                    </div>

                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between mb-1">
                        <h3 className="font-semibold text-white truncate">
                          {convo.name}
                        </h3>
                        <span className="text-xs text-slate-400">
                          {convo.lastSeen}
                        </span>
                      </div>

                      <p className="text-sm text-slate-300 truncate mb-2">
                        {convo.lastMessage}
                      </p>

                      <div className="flex items-center justify-between">
                        {convo.isGroup && (
                          <div className="flex items-center space-x-1">
                            <Users className="h-3 w-3 text-slate-400" />
                            <span className="text-xs text-slate-400">
                              {convo.participants.length} members
                            </span>
                          </div>
                        )}
                        {convo.unreadCount && (
                          <Badge className="bg-blue-600 text-white text-xs px-2 py-1 rounded-full">
                            {convo.unreadCount}
                          </Badge>
                        )}
                      </div>
                    </div>
                  </div>
                </Card>
              </motion.div>
            );
          })}
        </div>
      </ScrollArea>
    </div>
  );
}
