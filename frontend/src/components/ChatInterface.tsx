"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import {
  Send,
  Users,
  Search,
  MoreVertical,
  Phone,
  Video,
  Smile,
  Paperclip,
} from "lucide-react";

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

const participantsData: Participant[] = [
  {
    id: 1,
    name: "You",
    avatar:
      "https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&w=150&h=150&dpr=2",
    status: "online",
  },
  {
    id: 2,
    name: "Alice Cooper",
    avatar:
      "https://images.pexels.com/photos/415829/pexels-photo-415829.jpeg?auto=compress&cs=tinysrgb&w=150&h=150&dpr=2",
    status: "online",
  },
  {
    id: 3,
    name: "Bob Wilson",
    avatar:
      "https://images.pexels.com/photos/614810/pexels-photo-614810.jpeg?auto=compress&cs=tinysrgb&w=150&h=150&dpr=2",
    status: "away",
  },
  {
    id: 4,
    name: "Charlie Brown",
    avatar:
      "https://images.pexels.com/photos/91227/pexels-photo-91227.jpeg?auto=compress&cs=tinysrgb&w=150&h=150&dpr=2",
    status: "offline",
  },
  {
    id: 5,
    name: "David Miller",
    avatar:
      "https://images.pexels.com/photos/697509/pexels-photo-697509.jpeg?auto=compress&cs=tinysrgb&w=150&h=150&dpr=2",
    status: "online",
  },
];

const conversationsData: Conversation[] = [
  {
    id: 1,
    name: "Developer's battlefield",
    isGroup: true,
    participants: [
      participantsData[0],
      participantsData[1],
      participantsData[2],
      participantsData[3],
    ],
    lastMessage: "Let's meet online tonight.",
    unreadCount: 3,
    lastSeen: "10:04 AM",
    messages: [
      {
        id: 1,
        senderId: 2,
        text: "Hey team, ready for the exam? 📚",
        timestamp: "10:00 AM",
        status: "read",
      },
      {
        id: 2,
        senderId: 3,
        text: "Almost there! Need to revise the backend concepts.",
        timestamp: "10:02 AM",
        status: "read",
      },
      {
        id: 3,
        senderId: 4,
        text: "Let's meet online tonight for a final review session.",
        timestamp: "10:03 AM",
        status: "delivered",
      },
      {
        id: 4,
        senderId: 1,
        text: "I'm down for it! What time works for everyone?",
        timestamp: "10:04 AM",
        status: "sent",
      },
    ],
  },
  {
    id: 2,
    name: "Alice Cooper",
    isGroup: false,
    participants: [participantsData[1]],
    lastMessage: "All good! Just chilling.",
    lastSeen: "9:05 AM",
    messages: [
      {
        id: 5,
        senderId: 1,
        text: "Hey Alice, how's it going?",
        timestamp: "9:00 AM",
        status: "read",
      },
      {
        id: 6,
        senderId: 2,
        text: "All good! Just chilling on this beautiful day ☀️",
        timestamp: "9:05 AM",
        status: "delivered",
      },
    ],
  },
  {
    id: 2,
    name: "Charlie Brown",
    isGroup: false,
    participants: [participantsData[4]],
    lastMessage: "All good! Just chilling.",
    lastSeen: "9:05 AM",
    messages: [
      {
        id: 7,
        senderId: 1,
        text: "Hey Alice, how's it going?",
        timestamp: "9:00 AM",
        status: "read",
      },
      {
        id: 8,
        senderId: 4,
        text: "All good! Just chilling on this beautiful day ☀️",
        timestamp: "9:05 AM",
        status: "delivered",
      },
    ],
  },
];

export default function App() {
  const [selectedConversationId, setSelectedConversationId] =
    useState<number>(1);
  const [input, setInput] = useState("");
  const [searchQuery, setSearchQuery] = useState("");

  const selectedConversation = conversationsData.find(
    (c) => c.id === selectedConversationId
  )!;

  const filteredConversations = conversationsData.filter((convo) =>
    convo.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  function handleSend() {
    if (!input.trim()) return;
    // In a real app, this would send the message
    console.log(`Send message "${input}" to "${selectedConversation.name}"`);
    setInput("");
  }

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

  return (
    <div className="flex h-screen w-full bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="flex w-full bg-white shadow-2xl">
        {/* Sidebar */}
        <aside className="w-80 bg-white border-r border-slate-200 flex flex-col">
          {/* Header */}
          <div className="p-6 border-b border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <h1 className="text-2xl font-bold text-slate-900">Messages</h1>
              <Button
                variant="ghost"
                size="icon"
                className="text-slate-600 hover:text-slate-900"
              >
                <MoreVertical className="h-5 w-5" />
              </Button>
            </div>

            {/* Search */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 h-4 w-4" />
              <Input
                placeholder="Search conversations..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 bg-slate-50 border-slate-200 focus:bg-white transition-colors"
              />
            </div>
          </div>

          {/* Conversations List */}
          <ScrollArea className="flex-1">
            <div className="p-2">
              {filteredConversations.map((convo) => {
                const isSelected = convo.id === selectedConversationId;
                const mainParticipant = convo.isGroup
                  ? null
                  : convo.participants[0];

                return (
                  <Card
                    key={convo.id}
                    onClick={() => setSelectedConversationId(convo.id)}
                    className={`mb-2 p-4 cursor-pointer transition-all duration-200 hover:shadow-md border ${
                      isSelected
                        ? "bg-blue-50 border-blue-200 shadow-sm"
                        : "bg-white border-slate-200 hover:bg-slate-50"
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
                          <h3 className="font-semibold text-slate-900 truncate">
                            {convo.name}
                          </h3>
                          <span className="text-xs text-slate-500">
                            {convo.lastSeen}
                          </span>
                        </div>

                        <p className="text-sm text-slate-600 truncate mb-2">
                          {convo.lastMessage}
                        </p>

                        <div className="flex items-center justify-between">
                          {convo.isGroup && (
                            <div className="flex items-center space-x-1">
                              <Users className="h-3 w-3 text-slate-400" />
                              <span className="text-xs text-slate-500">
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
                );
              })}
            </div>
          </ScrollArea>
        </aside>

        {/* Chat Area */}
        <section className="flex flex-col flex-1 bg-slate-50">
          {/* Chat Header */}
          <div className="bg-white p-4 border-b border-slate-200 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Avatar className="w-10 h-10">
                {selectedConversation.isGroup ? (
                  <AvatarFallback className="bg-gradient-to-br from-blue-500 to-purple-600 text-white">
                    <Users className="h-5 w-5" />
                  </AvatarFallback>
                ) : (
                  <AvatarImage
                    src={selectedConversation.participants[0]?.avatar}
                    alt={selectedConversation.participants[0]?.name}
                  />
                )}
              </Avatar>

              <div>
                <h2 className="font-semibold text-slate-900">
                  {selectedConversation.name}
                </h2>
                <p className="text-sm text-slate-500">
                  {selectedConversation.isGroup
                    ? `${selectedConversation.participants.length} members`
                    : selectedConversation.participants[0]?.status || "offline"}
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <Button
                variant="ghost"
                size="icon"
                className="text-slate-600 hover:text-slate-900"
              >
                <Phone className="h-5 w-5" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                className="text-slate-600 hover:text-slate-900"
              >
                <Video className="h-5 w-5" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                className="text-slate-600 hover:text-slate-900"
              >
                <MoreVertical className="h-5 w-5" />
              </Button>
            </div>
          </div>

          {/* Messages Area */}
          <ScrollArea className="flex-1 p-6">
            <div className="space-y-6">
              {selectedConversation.messages.map((msg, index) => {
                const sender = participantsData.find(
                  (p) => p.id === msg.senderId
                );
                const isMe = sender?.id === 1;
                const showAvatar =
                  !isMe &&
                  (index === 0 ||
                    selectedConversation.messages[index - 1]?.senderId !==
                      msg.senderId);

                return (
                  <div
                    key={msg.id}
                    className={`flex ${isMe ? "justify-end" : "justify-start"}`}
                  >
                    <div
                      className={`flex max-w-xs lg:max-w-md ${
                        isMe ? "flex-row-reverse" : "flex-row"
                      } items-end space-x-2`}
                    >
                      {showAvatar && !isMe && (
                        <Avatar className="w-8 h-8">
                          <AvatarImage
                            src={sender?.avatar}
                            alt={sender?.name}
                          />
                          <AvatarFallback>{sender?.name?.[0]}</AvatarFallback>
                        </Avatar>
                      )}

                      <div className={`${showAvatar && !isMe ? "" : "ml-10"}`}>
                        {!isMe &&
                          selectedConversation.isGroup &&
                          showAvatar && (
                            <p className="text-xs text-slate-500 mb-1 ml-3">
                              {sender?.name}
                            </p>
                          )}

                        <div
                          className={`px-4 py-3 rounded-2xl shadow-sm ${
                            isMe
                              ? "bg-blue-600 text-white rounded-br-md"
                              : "bg-white text-slate-900 rounded-bl-md border border-slate-200"
                          }`}
                        >
                          <p className="text-sm leading-relaxed">{msg.text}</p>
                        </div>

                        <div
                          className={`flex items-center mt-1 space-x-1 ${
                            isMe ? "justify-end" : "justify-start"
                          }`}
                        >
                          <span className="text-xs text-slate-500">
                            {msg.timestamp}
                          </span>
                          {isMe && msg.status && (
                            <div
                              className={`w-2 h-2 rounded-full ${
                                msg.status === "read"
                                  ? "bg-blue-500"
                                  : msg.status === "delivered"
                                  ? "bg-slate-400"
                                  : "bg-slate-300"
                              }`}
                            />
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </ScrollArea>

          {/* Message Input */}
          <div className="bg-white p-4 border-t border-slate-200">
            <div className="flex items-end space-x-3">
              <Button
                variant="ghost"
                size="icon"
                className="text-slate-600 hover:text-slate-900 mb-2"
              >
                <Paperclip className="h-5 w-5" />
              </Button>

              <div className="flex-1 relative">
                <Input
                  type="text"
                  placeholder={`Message ${selectedConversation.name}...`}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && !e.shiftKey) {
                      e.preventDefault();
                      handleSend();
                    }
                  }}
                  className="pr-12 py-3 bg-slate-50 border-slate-200 focus:bg-white transition-colors"
                />
                <Button
                  variant="ghost"
                  size="icon"
                  className="absolute right-2 top-1/2 transform -translate-y-1/2 text-slate-600 hover:text-slate-900"
                >
                  <Smile className="h-4 w-4" />
                </Button>
              </div>

              <Button
                onClick={handleSend}
                disabled={!input.trim()}
                size="icon"
                className="bg-blue-600 hover:bg-blue-700 text-white rounded-full shadow-lg transition-all duration-200 hover:shadow-xl"
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
