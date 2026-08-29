# Privacy

Reco Box is a local desktop application. It does not require a Reco Box
account, does not include analytics, and does not upload the room list,
recording history, logs, or output videos to a Reco Box server.

The application stores its SQLite database, runtime logs, import reports and
upstream runtime files in the current Windows user's application-data folder.
Recordings are written only to the folders selected by the user.

Live-room URLs are sent only to the relevant livestream platform and the
network endpoints required by the pinned resolver. Resolved transient stream
URLs are used by FFmpeg/Qt Multimedia in memory and are deliberately removed
from application logging.

The pinned upstream resolver currently disables TLS certificate verification for
its main asynchronous platform requests. This compatibility behavior can reduce
protection against man-in-the-middle tampering of resolver responses and should
be treated as a medium-risk limitation. Use Reco Box on a trusted network. The
project will test restoring verification platform by platform and retain only
explicit, narrowly scoped exceptions where required for compatibility.

The legacy importer reads only the selected configuration files. It imports
room URLs and non-sensitive recording preferences; cookies, account tokens,
notification secrets and proxy credentials are not imported or included in
the import report.

Before reporting a bug, remove room URLs, streamer names, local file paths and
any platform response data from screenshots and logs.
