# Reco Box recording context

This context names the concepts that connect a monitored public livestream to
its local recording history. It keeps the logical broadcast distinct from the
individual process attempts used to capture it.

## Live recording lifecycle

**Live session**:
A single continuous occurrence of a public livestream for one monitored room.
It may contain several recording attempts while remaining one logical history item.
_Avoid_: FFmpeg process, recording file, recovery attempt

**Recording attempt**:
One capture effort within a live session. An attempt can end without ending the
live session, so it is not the identity of the broadcast itself.
_Avoid_: live session, history item

**Attempt output number**:
The next collision-free media-file number selected inside the stable session
directory. A recovery attempt advances this number without creating another
session directory.
_Avoid_: session ID, retry count, process ID

**Session directory**:
The stable local folder owned by one live session. Every attempt belonging to
that session writes under the same folder so the broadcast keeps one output layout.
_Avoid_: attempt directory, temporary folder

**Recording session**:
The durable identity of a live session, including its room, start time, stable
session directory, current attempt, lifecycle state, and recovery reason.
_Avoid_: recording row, FFmpeg process

**Recovery reason**:
A safe, stable classification explaining why the current recording attempt may
need another attempt. It is not a copy of a platform response or a transient
playback address.
_Avoid_: raw error text, stream URL

**Transient stream URL**:
The short-lived playback address resolved for one capture attempt. It is an
in-memory input only and is never part of the durable recording-session record.
_Avoid_: session URL, permanent stream URL
