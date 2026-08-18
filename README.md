# Communication Skills

AI agent skills for Israeli business communication: email, SMS, WhatsApp, job market, and team workflows.

Part of [Skills IL](https://github.com/skills-il) — curated AI agent skills for Israeli developers.

## Skills

| Skill | Description | Scripts | References |
|-------|-------------|---------|------------|
| [israeli-email-compliance](./israeli-email-compliance/) | Israeli email marketing compliance: Chok HaSpam (Amendment 40), Hebrew RTL templates, ISP deliverability, consent management, unsubscribe mechanisms. | `check_email.py` | 1 |
| [israeli-job-market](./israeli-job-market/) | Israeli job platforms (AllJobs, Drushim, JobMaster, LinkedIn Israel), Hebrew CV writing, salary benchmarks in NIS. | -- | 1 |
| [israeli-sms-gateway](./israeli-sms-gateway/) | Israeli SMS provider integration: SMS4Free, InforUMobile, Twilio. Phone validation, OTP, bulk messaging, compliance. | `validate_phone.py`, `send_sms.py` | -- |
| [israeli-whatsapp-automation](./israeli-whatsapp-automation/) | WhatsApp automation flows: chatbots, auto-replies, campaign scheduling, Shabbat/holiday-aware timing, Hebrew message templates, Israeli consumer opt-in rules. | -- | 1 |
| [israeli-whatsapp-business](./israeli-whatsapp-business/) | WhatsApp Business Cloud API for Israel: Hebrew templates, Shabbat-aware sending, anti-spam compliance, CRM integration. | `send_whatsapp.py` | -- |
| [monday-com-workflows](./monday-com-workflows/) | Monday.com optimization for Israeli teams: Sunday-Thursday sprints, Hebrew boards, holiday-aware automations, GraphQL API. | -- | 1 |

## Install

```bash
# Claude Code - install a specific skill
claude install github:skills-il/communication/israeli-sms-gateway

# Or clone the full repo
git clone https://github.com/skills-il/communication.git
```

## Contributing

See the org-level [Contributing Guide](https://github.com/skills-il/.github/blob/main/CONTRIBUTING.md).

## License

MIT

---

Built with care in Israel.
