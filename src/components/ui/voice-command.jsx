import * as React from "react";
import { cn } from "@/lib/utils";

const VoiceCommand = React.forwardRef(
  ({ className, userCommand, ...props }, ref) => {
    return (
      <textarea
        readOnly
        className={cn(
          "flex min-h-10 w-full max-w-lg resize-none overflow-hidden rounded-md border border-slate-200 bg-white px-3 py-2 text-sm ring-offset-white file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-slate-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-950 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-800 dark:bg-slate-950 dark:ring-offset-slate-950 dark:placeholder:text-slate-400 dark:focus-visible:ring-slate-300",
          className
        )}
        value={userCommand}
        ref={ref}
        {...props}
      />
    );
  }
);
VoiceCommand.displayName = "VoiceCommand";

export { VoiceCommand };
