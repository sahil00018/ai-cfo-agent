import { useEffect, useRef, useState } from "react";
import {
  Box,
  Paper,
  Typography,
  TextField,
  IconButton,
  CircularProgress,
  Chip,
  Stack,
  Avatar,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import DeleteIcon from "@mui/icons-material/Delete";
import SmartToyOutlinedIcon from "@mui/icons-material/SmartToyOutlined";
import PersonIcon from "@mui/icons-material/Person";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import { useChat } from "../../context/ChatContext";
import { askAgent } from "../../api/chatApi";
import { chartColors } from "../../theme/colors";

function formatCurrency(value) {
  return `₹${Number(value).toLocaleString("en-IN", { maximumFractionDigits: 0 })}`;
}

const SERIES_LABELS = {
  revenue: "Revenue",
  expenses: "Expenses",
  ebitda: "EBITDA",
  cash_position: "Cash Position",
  budget: "Budget",
};

function ChartBlock({ chart }) {
  if (!chart || !chart.data || chart.data.length === 0) return null;

  const isBar = chart.type === "bar";
  const ChartComponent = isBar ? BarChart : LineChart;

  return (
    <Paper
      variant="outlined"
      sx={{
        p: 2,
        mb: 2,
        bgcolor: "background.paper",
      }}
    >
      {chart.title && (
        <Typography variant="subtitle2" sx={{ mb: 1.5, fontWeight: 600 }}>
          {chart.title}
        </Typography>
      )}

      <Box sx={{ width: "100%", height: 240 }}>
        <ResponsiveContainer width="100%" height="100%">
          <ChartComponent data={chart.data} margin={{ left: 0, right: 8, top: 4, bottom: 4 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey={chart.x_key || "month"} tick={{ fontSize: 11 }} />
            <YAxis
              tick={{ fontSize: 11 }}
              width={60}
              tickFormatter={(v) => `₹${(v / 1000).toFixed(0)}k`}
            />
            <Tooltip formatter={(v) => formatCurrency(v)} />
            <Legend wrapperStyle={{ fontSize: 12 }} />
            {chart.series.map((key, i) =>
              isBar ? (
                <Bar
                  key={key}
                  dataKey={key}
                  name={SERIES_LABELS[key] || key}
                  fill={chartColors[i % chartColors.length]}
                  radius={[4, 4, 0, 0]}
                />
              ) : (
                <Line
                  key={key}
                  type="monotone"
                  dataKey={key}
                  name={SERIES_LABELS[key] || key}
                  stroke={chartColors[i % chartColors.length]}
                  strokeWidth={2}
                  dot={{ r: 2 }}
                />
              )
            )}
          </ChartComponent>
        </ResponsiveContainer>
      </Box>
    </Paper>
  );
}

function AgentAnswer({ result }) {
  if (!result) return null;

  const {
    agent,
    analysis,
    recommendation,
    ai_insight,
    ai_report,
    executive_summary,
    chart,
    charts,
    ...rest
  } = result;

  const extraEntries = Object.entries(rest).filter(
    ([key, value]) =>
      ![
        "agent",
        "analysis",
        "recommendation",
        "ai_insight",
        "ai_report",
        "executive_summary",
        "chart",
        "charts",
        "financial_data",
        "recommended_actions",
        "execution",
      ].includes(key) &&
      typeof value !== "object"
  );

  return (
    <Box sx={{ width: "100%" }}>
      {agent && (
        <Chip
          label={agent}
          color="primary"
          size="small"
          sx={{
            mb: 2,
            fontWeight: 600,
          }}
        />
      )}

      {analysis && (
        <Typography
          variant="body2"
          sx={{
            mb: 2,
            lineHeight: 1.8,
            whiteSpace: "pre-wrap",
            wordBreak: "break-word",
          }}
        >
          {analysis}
        </Typography>
      )}

      {ai_report && (
        <Typography
          variant="body2"
          sx={{
            mb: 2,
            lineHeight: 1.8,
            whiteSpace: "pre-wrap",
            wordBreak: "break-word",
          }}
        >
          {ai_report}
        </Typography>
      )}

      {/* Single chart (FP&A / Treasury / Budget agents) */}
      {chart && <ChartBlock chart={chart} />}

      {/* Multiple charts (Reporting agent) */}
      {Array.isArray(charts) && charts.map((c, i) => <ChartBlock key={i} chart={c} />)}

      {ai_insight && (
        <Paper
          sx={{
            bgcolor: "#f8fafc",
            p: 2,
            mb: 2,
          }}
        >
          <Typography
            variant="body2"
            color="text.secondary"
          >
            {ai_insight}
          </Typography>
        </Paper>
      )}

      {executive_summary && (
        <Paper
          variant="outlined"
          sx={{
            p: 2,
            mb: 2,
            bgcolor: "#fafafa",
          }}
        >
          <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 600 }}>
            Executive Summary
          </Typography>
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{ whiteSpace: "pre-wrap" }}
          >
            {executive_summary}
          </Typography>
        </Paper>
      )}

      {Array.isArray(result.recommended_actions) && result.recommended_actions.length > 0 && (
        <Paper
          variant="outlined"
          sx={{ p: 2, mb: 2, bgcolor: "#fafafa" }}
        >
          <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 600 }}>
            Recommended Actions
          </Typography>
          <Stack spacing={0.5}>
            {result.recommended_actions.map((action, i) => (
              <Typography key={i} variant="body2">• {action}</Typography>
            ))}
          </Stack>
        </Paper>
      )}

      {extraEntries.length > 0 && (
        <Paper
          variant="outlined"
          sx={{
            p: 2,
            mb: 2,
            bgcolor: "#fafafa",
          }}
        >
          <Typography
            variant="subtitle2"
            sx={{
              mb: 1.5,
              fontWeight: 600,
            }}
          >
            Financial Metrics
          </Typography>

          <Stack spacing={1}>
            {extraEntries.map(([key, value]) => (
              <Box
                key={key}
                sx={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  flexWrap: "wrap",
                  gap: 1,
                  borderBottom: "1px solid #eee",
                  pb: 1,
                }}
              >
                <Typography
                  variant="body2"
                  color="text.secondary"
                  sx={{
                    textTransform: "capitalize",
                  }}
                >
                  {key.replace(/_/g, " ")}
                </Typography>

                <Typography
                  variant="body2"
                  fontWeight={600}
                >
                  {typeof value === "number"
                    ? formatCurrency(value)
                    : String(value)}
                </Typography>
              </Box>
            ))}
          </Stack>
        </Paper>
      )}

      {recommendation && (
        <Paper
          sx={{
            bgcolor: "#E8F5E9",
            borderLeft: "5px solid green",
            p: 2,
          }}
        >
          <Typography
            variant="subtitle2"
            color="success.main"
            fontWeight={700}
            gutterBottom
          >
            Recommendation
          </Typography>

          <Typography variant="body2">
            {recommendation}
          </Typography>
        </Paper>
      )}
    </Box>
  );
}

export default function Chat() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const { messages, addMessage, clearMessages } = useChat();
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleAsk() {
    const q = question.trim();
    if (!q || loading) return;

    addMessage({ role: "user", text: q });
    setQuestion("");
    setLoading(true);

    try {
      const res = await askAgent(q);
      addMessage({ role: "agent", result: res });
    } catch (err) {
      addMessage({ role: "agent", error: true, text: "I couldn't process that question. Please try again." });
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleAsk();
    }
  }

  return (
    <Box sx={{ display: "flex", flexDirection: "column", height: "calc(100vh - 112px)" }}>
      <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h4">AI CFO Assistant</Typography>
        {messages.length > 0 && (
          <IconButton
            size="small"
            onClick={clearMessages}
            title="Clear conversation"
            sx={{ color: "text.secondary" }}
          >
            <DeleteIcon fontSize="small" />
          </IconButton>
        )}
      </Stack>
      <Box
        sx={{
          flexGrow: 1,
          overflowY: "auto",
          pr: 0.5,
          mb: 2,
        }}
      >
        {messages.length === 0 && (
          <Paper
            variant="outlined"
            sx={{ p: 3, borderRadius: 3, textAlign: "center", color: "text.secondary" }}
          >
            <SmartToyOutlinedIcon sx={{ fontSize: 40, mb: 1, opacity: 0.5 }} />
            <Typography>Ask about revenue, cash flow, budgets, compliance, risk, or company health.</Typography>
          </Paper>
        )}

        <Stack spacing={2}>
          {messages.map((msg, i) => (
            <Stack
              key={i}
              direction={msg.role === "user" ? "row-reverse" : "row"}
              spacing={1.5}
              alignItems="flex-start"
            >
              <Avatar
                sx={{
                  width: 32,
                  height: 32,
                  bgcolor: msg.role === "user" ? "secondary.main" : "primary.main",
                }}
              >
                {msg.role === "user" ? <PersonIcon fontSize="small" /> : <SmartToyOutlinedIcon fontSize="small" />}
              </Avatar>

              <Paper
                sx={{
                  p: 2,
                  borderRadius: 3,
                  width: "100%",
                  maxWidth: {
                    xs: "90%",
                    md: "70%",
                  },
                  bgcolor:
                    msg.role === "user"
                      ? "primary.main"
                      : "background.paper",
                  color:
                    msg.role === "user"
                      ? "#fff"
                      : "text.primary",
                  border:
                    msg.role === "agent"
                      ? "1px solid #E5E9EF"
                      : "none",
                  overflow: "hidden",
                  wordBreak: "break-word",
                  boxSizing: "border-box",
                }}
              >
                {msg.role === "user" ? (
                  <Typography variant="body2">{msg.text}</Typography>
                ) : msg.error ? (
                  <Typography variant="body2" color="error">{msg.text}</Typography>
                ) : (
                  <AgentAnswer result={msg.result} />
                )}
              </Paper>
            </Stack>
          ))}

          {loading && (
            <Stack direction="row" spacing={1.5} alignItems="center">
              <Avatar sx={{ width: 32, height: 32, bgcolor: "primary.main" }}>
                <SmartToyOutlinedIcon fontSize="small" />
              </Avatar>
              <CircularProgress size={20} />
            </Stack>
          )}
        </Stack>

        <div ref={bottomRef} />
      </Box>

      <Paper
        sx={{
          p: 1,
          borderRadius: 3,
          display: "flex",
          alignItems: "flex-end",
          gap: 1,
          border: "1px solid #E5E9EF",
        }}
        elevation={0}
      >
        <TextField
          fullWidth
          multiline
          maxRows={4}
          placeholder="Ask a financial question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
          variant="standard"
          InputProps={{ disableUnderline: true }}
          sx={{ px: 1 }}
        />
        <IconButton color="primary" onClick={handleAsk} disabled={loading || !question.trim()}>
          <SendIcon />
        </IconButton>
      </Paper>
    </Box>
  );
}