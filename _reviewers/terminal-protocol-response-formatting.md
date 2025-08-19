---
title: Protocol response formatting
description: When implementing terminal protocol responses (CSI, DCS, OSC sequences),
  ensure proper formatting with correct terminators and maintain protocol transparency.
  Terminal protocols require specific response formats with appropriate terminators
  - CSI responses should use the same C1 mode as the request, DCS responses need proper
  DCS/ST framing, and OSC...
repository: microsoft/terminal
label: Networking
language: C++
comments_count: 2
repository_stars: 99242
---

When implementing terminal protocol responses (CSI, DCS, OSC sequences), ensure proper formatting with correct terminators and maintain protocol transparency. Terminal protocols require specific response formats with appropriate terminators - CSI responses should use the same C1 mode as the request, DCS responses need proper DCS/ST framing, and OSC responses should echo the same terminator (BEL or ST) as the requesting sequence.

For example, when handling terminal state reports:

```cpp
void AdaptDispatch::_ReturnDcsResponse(const std::wstring_view response) const
{
    const auto dcs = _terminalInput.GetInputMode(TerminalInput::Mode::SendC1) ? L"\x90" : L"\x1BP";
    const auto st = _terminalInput.GetInputMode(TerminalInput::Mode::SendC1) ? L"\x9C" : L"\x1B\\";
    _api.ReturnResponse(fmt::format(FMT_COMPILE(L"{}{}{}"), dcs, response, st));
}
```

Additionally, maintain protocol transparency by avoiding reactions to sequences that should be handled by the terminal client. ConPTY should not react to sequences like "CSI 1 t" or "CSI 2 t" for show/hide operations, as these are the terminal's responsibility. This prevents double-processing and maintains the expected protocol behavior between terminal and application.