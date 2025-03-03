import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

type InputWithButtonProps = {
  btnText: string;
  placeholderText: string;
  onSubmit: () => void;
  onChange: (value: string) => void;
};

export const InputWithButton= ({
  btnText,
  placeholderText,
  onSubmit,
  onChange,
}: InputWithButtonProps) => {
  return (
    <div className="flex w-full items-center space-x-2">
      <Input type="text" placeholder={placeholderText} onChange={(e) => onChange(e.target.value)} />
      <Button type="button" onClick={onSubmit}>
        {btnText}
      </Button>
    </div>
  );
};
