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

The legacy importer reads only the selected configuration files. It imports
room URLs and non-sensitive recording preferences; cookies, account tokens,
notification secrets and proxy credentials are not imported or included in
the import report.

Before reporting a bug, remove room URLs, streamer names, local file paths and
any platform response data from screenshots and logs.
