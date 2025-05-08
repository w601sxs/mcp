import { Bot, Send } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetDescription, SheetTrigger } from "@/components/ui/sheet"
import { Textarea } from "@/components/ui/textarea"

export function ChatSidebar() {
  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button
          variant="default"
          size="default"
          className="fixed bottom-4 right-4 h-12 rounded-full shadow-lg bg-primary text-primary-foreground hover:bg-primary/90 px-4 gap-2"
        >
          <Bot className="h-5 w-5" />
          <span className="hidden sm:inline">Chat with AI</span>
        </Button>
      </SheetTrigger>
      <SheetContent side="right" className="w-[400px] sm:w-[540px] p-0 flex flex-col h-screen">
        <SheetHeader className="px-6 py-4 border-b">
          <SheetTitle>AI Assistant</SheetTitle>
          <SheetDescription>Chat with our AI assistant for help and support.</SheetDescription>
        </SheetHeader>
        <div className="flex flex-col flex-1 overflow-hidden">
          <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
            {/* Chat messages skeleton */}
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <Skeleton className="h-8 w-8 rounded-full" />
                <div className="space-y-2">
                  <Skeleton className="h-4 w-[200px]" />
                  <Skeleton className="h-4 w-[150px]" />
                </div>
              </div>
              <div className="flex items-start gap-3">
                <Skeleton className="h-8 w-8 rounded-full" />
                <div className="space-y-2">
                  <Skeleton className="h-4 w-[250px]" />
                  <Skeleton className="h-4 w-[200px]" />
                </div>
              </div>
            </div>
          </div>
          <div className="border-t p-4">
            <div className="flex gap-2">
              <Textarea
                placeholder="Type your message..."
                className="min-h-[60px] resize-none"
              />
              <Button size="icon" className="h-[60px] w-[60px]">
                <Send className="h-5 w-5" />
              </Button>
            </div>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  )
} 