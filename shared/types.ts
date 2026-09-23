export type StepStatus = "pending" | "running" | "done" | "error";

export interface AuditStep {
  id: string;
  name: string;
  status: StepStatus;
  resultPath?: string;
  error?: string;
  startedAt?: string;
  finishedAt?: string;
}

export interface AuditSession {
  id: string;
  repoUrl: string;
  repoName: string;
  repoPath: string;
  resultsDir: string;
  status: "idle" | "running" | "completed" | "error";
  steps: AuditStep[];
  errorMsg?: string;
  createdAt: string;
  updatedAt: string;
}

export interface SSEEvent {
  step: string;
  status: StepStatus;
  log?: string;
  resultPath?: string;
  error?: string;
}

export interface AuditResult {
  files: string[];
}
