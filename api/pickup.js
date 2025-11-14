import fetch from "node-fetch";

export default async function handler(req, res) {
  const part = req.query.part || "MG6K4HN/A";   // iPhone 17 white example
  const pin = req.query.pin || "110017";

  const APPLE_COOKIES = process.env.APPLE_COOKIES; // Your manually pasted cookies
  const USER_AGENT = process.env.USER_AGENT;       // Your real browser UA

  if (!APPLE_COOKIES || !USER_AGENT) {
    return res.status(500).json({ error: "Missing env APPLE_COOKIES or USER_AGENT" });
  }

  const url = `https://www.apple.com/in/shop/fulfillment-messages?fae=true&little=false&parts.0=${part}&mts.0=regular&mts.1=sticky&fts=true`;

  const headers = {
    "User-Agent": USER_AGENT,
    "Accept": "*/*",
    "Referer": "https://www.apple.com/in/shop",
    "x-skip-redirect": "true",
    "Cookie": APPLE_COOKIES,
  };

  const response = await fetch(url, { headers });
  const text = await response.text();

  if (response.status !== 200) {
    return res.status(500).json({
      status: response.status,
      message: "Apple blocked request",
      body: text,
    });
  }

  // try parsing json
  try {
    const json = JSON.parse(text);
    return res.status(200).json(json);
  } catch (e) {
    return res.status(500).json({ error: "Failed to parse JSON", raw: text });
  }
}
