import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const inputVariants = cva(
    "inline-flex items-center gap-2 w-full rounded-md text-sm transition-all [&_svg]:shrink-0 outline-none disabled:cursor-not-allowed disabled:opacity-50 focus:ring-2 focus:ring-offset-2 aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40",
    {
        variants: {
            variant: {
                default:
                    "bg-background text-foreground border border-input shadow-xs hover:border-primary/50 focus:border-primary focus:ring-primary/10 dark:bg-input/30 dark:border-input",
                outline:
                    "bg-transparent border border-input shadow-xs hover:border-primary/50 focus:border-primary focus:ring-primary/10 dark:border-input/70",
                filled:
                    "bg-accent text-accent-foreground border-none shadow-xs hover:bg-accent/80 focus:ring-accent/20 dark:bg-input/50",
                ghost:
                    "bg-transparent border-none hover:bg-accent/50 focus:ring-accent/10 dark:hover:bg-accent/30",
                flush:
                    "bg-transparent border-none border-b border-input/50 rounded-none focus:border-b-primary focus:ring-0 shadow-none hover:border-b-primary",
            },
            inputSize: { // 改为 inputSize 避免冲突
                default: "h-9 px-3 py-2",
                sm: "h-8 px-2.5 py-1.5 text-xs",
                lg: "h-10 px-4 py-2.5",
                icon: "h-9 px-3 py-2 [&>svg]:size-4",
            },
            hasIcon: {
                true: "pl-9",
            },
        },
        compoundVariants: [
            {
                inputSize: "sm",
                hasIcon: true,
                class: "pl-7",
            },
            {
                inputSize: "lg",
                hasIcon: true,
                class: "pl-11",
            },
        ],
        defaultVariants: {
            variant: "default",
            inputSize: "default",
        },
    }
);

export interface InputProps
    extends Omit<React.InputHTMLAttributes<HTMLInputElement>, "size">, // 排除原生 size
        VariantProps<typeof inputVariants> {
    icon?: React.ReactNode;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
    ({ className, variant, inputSize, hasIcon, icon, ...props }, ref) => {
        const hasIconSlot = !!icon || hasIcon;

        return (
            <div className="relative">
                {icon && (
                    <span className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground">
            {icon}
          </span>
                )}
                <input
                    ref={ref}
                    className={cn(
                        inputVariants({ variant, inputSize, hasIcon: hasIconSlot, className })
                    )}
                    {...props}
                />
            </div>
        );
    }
);
Input.displayName = "Input";

export { Input, inputVariants };