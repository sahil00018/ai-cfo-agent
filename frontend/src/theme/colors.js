export const colors = {
  primary: "#1976D2",
  secondary: "#1565C0",
  success: "#2E7D32",
  warning: "#ED6C02",
  error: "#D32F2F",
  background: "#F5F7FA",
  paper: "#FFFFFF",
  textPrimary: "#212121",
  textSecondary: "#757575",
};

// Extra tokens used by charts/status chips, kept separate so the
// core MUI palette above stays untouched.
export const chartColors = ["#1976D2", "#2E7D32", "#ED6C02", "#9333EA", "#0EA5E9", "#D32F2F"];

export const statusColors = {
  Pending: { bg: "#FFF4E5", fg: "#B76E00" },
  "In Progress": { bg: "#E7F1FE", fg: "#1565C0" },
  Completed: { bg: "#E9F7EF", fg: "#1E7B34" },
  Blocked: { bg: "#FDEAEA", fg: "#B3261E" },
};

export const priorityColors = {
  Low: { bg: "#EEF2F6", fg: "#546679" },
  Medium: { bg: "#FFF4E5", fg: "#B76E00" },
  High: { bg: "#FDEAEA", fg: "#B3261E" },
};