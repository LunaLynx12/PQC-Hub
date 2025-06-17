import { useState } from 'react';
import { motion } from 'framer-motion';
import ContactsSidebar from '@/components/ContactsSidebar';
import ChatArea from '@/components/ChatArea';
import AnimatedBackground from '@/components/AnimatedBackground';

interface Participant {
  id: number;
  name: string;
  avatar?: string;
  status?: 'online' | 'offline' | 'away';
}

interface Message {
  id: number;
  senderId: number;
  text: string;
  timestamp: string;
  status?: 'sent' | 'delivered' | 'read';
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
    name: 'You',
    avatar: 'https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&w=150&h=150&dpr=2',
    status: 'online',
  },
  {
    id: 2,
    name: 'Alice Cooper',
    avatar: 'https://images.pexels.com/photos/415829/pexels-photo-415829.jpeg?auto=compress&cs=tinysrgb&w=150&h=150&dpr=2',
    status: 'online',
  },
  {
    id: 3,
    name: 'Bob Wilson',
    avatar: 'https://images.pexels.com/photos/614810/pexels-photo-614810.jpeg?auto=compress&cs=tinysrgb&w=150&h=150&dpr=2',
    status: 'away',
  },
  {
    id: 4,
    name: 'Charlie Brown',
    avatar: 'https://images.pexels.com/photos/91227/pexels-photo-91227.jpeg?auto=compress&cs=tinysrgb&w=150&h=150&dpr=2',
    status: 'offline',
  },
  {
    id: 5,
    name: 'David Miller',
    avatar: 'https://images.pexels.com/photos/697509/pexels-photo-697509.jpeg?auto=compress&cs=tinysrgb&w=150&h=150&dpr=2',
    status: 'online',
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
    lastSeen: '10:04 AM',
    messages: [
      {
        id: 1,
        senderId: 2,
        text: 'Hey team, ready for the exam? 📚',
        timestamp: '10:00 AM',
        status: 'read',
      },
      {
        id: 2,
        senderId: 3,
        text: 'Almost there! Need to revise the backend concepts.',
        timestamp: '10:02 AM',
        status: 'read',
      },
      {
        id: 3,
        senderId: 4,
        text: "Let's meet online tonight for a final review session.",
        timestamp: '10:03 AM',
        status: 'delivered',
      },
      {
        id: 4,
        senderId: 1,
        text: "I'm down for it! What time works for everyone?",
        timestamp: '10:04 AM',
        status: 'sent',
      },
    ],
  },
  {
    id: 2,
    name: 'Alice Cooper',
    isGroup: false,
    participants: [participantsData[1]],
    lastMessage: 'All good! Just chilling.',
    lastSeen: '9:05 AM',
    messages: [
      {
        id: 5,
        senderId: 1,
        text: "Hey Alice, how's it going?",
        timestamp: '9:00 AM',
        status: 'read',
      },
      {
        id: 6,
        senderId: 2,
        text: 'All good! Just chilling on this beautiful day ☀️',
        timestamp: '9:05 AM',
        status: 'delivered',
      },
    ],
  },
  {
    id: 3,
    name: 'Charlie Brown',
    isGroup: false,
    participants: [participantsData[3]],
    lastMessage: 'All good! Just chilling.',
    lastSeen: '9:05 AM',
    messages: [
      {
        id: 7,
        senderId: 1,
        text: "Hey Charlie, how's it going?",
        timestamp: '9:00 AM',
        status: 'read',
      },
      {
        id: 8,
        senderId: 4,
        text: 'All good! Just chilling on this beautiful day ☀️',
        timestamp: '9:05 AM',
        status: 'delivered',
      },
    ],
  },
];

export default function App() {
  const [selectedConversationId, setSelectedConversationId] = useState<number>(1);

  const selectedConversation = conversationsData.find(
    (c) => c.id === selectedConversationId
  )!;

  function handleSendMessage(message: string) {
    // In a real app, this would send the message
    console.log(`Send message "${message}" to "${selectedConversation.name}"`);
  }

  return (
    <div className="relative flex h-screen w-full bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 overflow-hidden">
      <AnimatedBackground />
      
      <motion.div
        initial={{ scale: 0.95, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.6, ease: 'easeOut' }}
        className="relative z-10 flex w-full h-full bg-white/10 backdrop-blur-xl border border-white/20 shadow-2xl"
      >
        {/* Decorative corner elements */}
        <div className="absolute -top-1 -left-1 w-3 h-3 bg-blue-500 rounded-full animate-pulse" />
        <div className="absolute -top-1 -right-1 w-3 h-3 bg-purple-500 rounded-full animate-pulse delay-300" />
        <div className="absolute -bottom-1 -left-1 w-3 h-3 bg-green-500 rounded-full animate-pulse delay-700" />
        <div className="absolute -bottom-1 -right-1 w-3 h-3 bg-pink-500 rounded-full animate-pulse delay-1000" />

        {/* Contacts Sidebar - Fixed width */}
        <div className="w-80 flex-shrink-0 h-full">
          <ContactsSidebar
            conversations={conversationsData}
            selectedConversationId={selectedConversationId}
            onSelectConversation={setSelectedConversationId}
          />
        </div>

        {/* Chat Area - Takes remaining space */}
        <div className="flex-1 h-full">
          <ChatArea
            conversation={selectedConversation}
            participants={participantsData}
            onSendMessage={handleSendMessage}
          />
        </div>
      </motion.div>
    </div>
  );
}