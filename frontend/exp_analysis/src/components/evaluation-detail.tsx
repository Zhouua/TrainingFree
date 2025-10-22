"use client";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import {
  Table,
  TableBody,
  TableCell,
  TableRow,
} from "@/components/ui/table";

type Evaluation = {
  id: number;
  exp_id: string;
  source: string;
  raw_question: string;
  level: number | null;
  augmented_question: string | null;
  correct_answer: string | null;
  file_name: string | null;
  stage: string;
  response: string | null;
  time_cost: number | null;
  trajectory: string | null;
  extracted_final_answer: string | null;
  judged_response: string | null;
  reasoning: string | null;
  correct: boolean | null;
  confidence: number | null;
};

interface EvaluationDetailProps {
  evaluation: Evaluation | null;
  isOpen: boolean;
  onClose: () => void;
}

export function EvaluationDetail({
  evaluation,
  isOpen,
  onClose,
}: EvaluationDetailProps) {
  if (!evaluation) {
    return null;
  }

  let parsedTrajectory: unknown = null; // Change from any to unknown
  try {
    if (evaluation.trajectory) {
      parsedTrajectory = JSON.parse(evaluation.trajectory);
    }
  } catch (error) {
    console.error("Failed to parse trajectory JSON:", error);
    parsedTrajectory = null; // Reset if parsing fails
  }

  const otherFields = [
    { label: "Experiment ID", value: evaluation.exp_id },
    { label: "File Name", value: evaluation.file_name },
    { label: "Augmented Question", value: evaluation.augmented_question },
    { label: "Time Cost", value: evaluation.time_cost },
    { label: "Extracted Final Answer", value: evaluation.extracted_final_answer },
    { label: "Judged Response", value: evaluation.judged_response },
    { label: "Reasoning", value: evaluation.reasoning },
  ];

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Evaluation Details (ID: {evaluation.id})</DialogTitle>
          <DialogDescription>Detailed information for the selected evaluation entry.</DialogDescription>
        </DialogHeader>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Left Column: Other Fields */}
          <div>
            <h3 className="text-lg font-semibold mb-2">General Information</h3>
            <Table>
              <TableBody>
                {otherFields.map((field) => (
                  <TableRow key={field.label}>
                    <TableCell className="font-medium w-1/3">{field.label}</TableCell>
                    <TableCell className="w-2/3 break-words">{String(field.value)}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>

          {/* Right Column: Trajectory */}
          <div>
            <h3 className="text-lg font-semibold mb-2">Trajectory</h3>
            {parsedTrajectory ? (
              <div className="bg-gray-100 dark:bg-gray-800 p-3 rounded-md text-sm overflow-auto max-h-[400px]">
                <pre className="whitespace-pre-wrap">
                  {JSON.stringify(parsedTrajectory, null, 2)}
                </pre>
              </div>
            ) : (
              <p className="text-gray-500 dark:text-gray-400">No trajectory data or invalid JSON.</p>
            )}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}