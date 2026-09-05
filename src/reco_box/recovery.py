from __future__ import annotations

from enum import StrEnum


class RecoveryState(StrEnum):
    """Runtime lifecycle states for one monitored room."""

    IDLE = "idle"
    CHECKING = "checking"
    PREPARING = "preparing"
    RECORDING = "recording"
    RECOVERING = "recovering"
    CONFIRMING_OFFLINE = "confirming_offline"
    CONVERTING = "converting"
    OFFLINE = "offline"
    ERROR = "error"
    STOPPING = "stopping"
    DISABLED = "disabled"


class RecoveryEvent(StrEnum):
    """Inputs that are allowed to move a room through its lifecycle."""

    CHECK_REQUESTED = "check_requested"
    ROOM_ENABLED = "room_enabled"
    ROOM_DISABLED = "room_disabled"
    LIVE_DETECTED = "live_detected"
    STREAM_OFFLINE = "stream_offline"
    RESOLVER_FAILED = "resolver_failed"
    RECORDING_STARTED = "recording_started"
    RECORDING_FINISHED = "recording_finished"
    RECORDING_FAILED = "recording_failed"
    CONVERSION_STARTED = "conversion_started"
    CONVERSION_SUCCEEDED = "conversion_succeeded"
    CONVERSION_FAILED = "conversion_failed"
    RECOVERY_EXHAUSTED = "recovery_exhausted"
    MANUAL_STOP_REQUESTED = "manual_stop_requested"
    STOP_COMPLETED = "stop_completed"
    PAUSE_COMPLETED = "pause_completed"
    PROTECTIVE_FAILURE = "protective_failure"


class InvalidRecoveryTransition(ValueError):
    """Raised when an event is not legal for the current lifecycle state."""

    def __init__(self, state: RecoveryState, event: RecoveryEvent) -> None:
        self.state = state
        self.event = event
        super().__init__(f"{event.value} is not valid from {state.value}")


_TRANSITIONS: dict[RecoveryState, dict[RecoveryEvent, RecoveryState]] = {
    RecoveryState.IDLE: {
        RecoveryEvent.CHECK_REQUESTED: RecoveryState.CHECKING,
        RecoveryEvent.ROOM_ENABLED: RecoveryState.OFFLINE,
        RecoveryEvent.ROOM_DISABLED: RecoveryState.DISABLED,
        RecoveryEvent.LIVE_DETECTED: RecoveryState.PREPARING,
        RecoveryEvent.STREAM_OFFLINE: RecoveryState.OFFLINE,
        RecoveryEvent.RESOLVER_FAILED: RecoveryState.RECOVERING,
        RecoveryEvent.PROTECTIVE_FAILURE: RecoveryState.ERROR,
    },
    RecoveryState.CHECKING: {
        RecoveryEvent.LIVE_DETECTED: RecoveryState.PREPARING,
        RecoveryEvent.STREAM_OFFLINE: RecoveryState.OFFLINE,
        RecoveryEvent.RESOLVER_FAILED: RecoveryState.RECOVERING,
        RecoveryEvent.ROOM_DISABLED: RecoveryState.DISABLED,
        RecoveryEvent.MANUAL_STOP_REQUESTED: RecoveryState.STOPPING,
        RecoveryEvent.PROTECTIVE_FAILURE: RecoveryState.ERROR,
    },
    RecoveryState.PREPARING: {
        RecoveryEvent.LIVE_DETECTED: RecoveryState.PREPARING,
        RecoveryEvent.RECORDING_STARTED: RecoveryState.RECORDING,
        RecoveryEvent.RECORDING_FINISHED: RecoveryState.CONFIRMING_OFFLINE,
        RecoveryEvent.CONVERSION_STARTED: RecoveryState.CONVERTING,
        RecoveryEvent.RECORDING_FAILED: RecoveryState.RECOVERING,
        RecoveryEvent.RECOVERY_EXHAUSTED: RecoveryState.ERROR,
        RecoveryEvent.STREAM_OFFLINE: RecoveryState.OFFLINE,
        RecoveryEvent.RESOLVER_FAILED: RecoveryState.RECOVERING,
        RecoveryEvent.ROOM_DISABLED: RecoveryState.DISABLED,
        RecoveryEvent.MANUAL_STOP_REQUESTED: RecoveryState.STOPPING,
        RecoveryEvent.PROTECTIVE_FAILURE: RecoveryState.ERROR,
    },
    RecoveryState.RECORDING: {
        RecoveryEvent.RECORDING_STARTED: RecoveryState.RECORDING,
        RecoveryEvent.RECORDING_FINISHED: RecoveryState.CONFIRMING_OFFLINE,
        RecoveryEvent.RECORDING_FAILED: RecoveryState.RECOVERING,
        RecoveryEvent.CONVERSION_STARTED: RecoveryState.CONVERTING,
        RecoveryEvent.RECOVERY_EXHAUSTED: RecoveryState.ERROR,
        RecoveryEvent.MANUAL_STOP_REQUESTED: RecoveryState.STOPPING,
        RecoveryEvent.PROTECTIVE_FAILURE: RecoveryState.ERROR,
    },
    RecoveryState.RECOVERING: {
        RecoveryEvent.CHECK_REQUESTED: RecoveryState.CHECKING,
        RecoveryEvent.LIVE_DETECTED: RecoveryState.PREPARING,
        RecoveryEvent.STREAM_OFFLINE: RecoveryState.OFFLINE,
        RecoveryEvent.RESOLVER_FAILED: RecoveryState.RECOVERING,
        RecoveryEvent.RECORDING_FAILED: RecoveryState.RECOVERING,
        RecoveryEvent.RECOVERY_EXHAUSTED: RecoveryState.ERROR,
        RecoveryEvent.ROOM_DISABLED: RecoveryState.DISABLED,
        RecoveryEvent.MANUAL_STOP_REQUESTED: RecoveryState.STOPPING,
        RecoveryEvent.PROTECTIVE_FAILURE: RecoveryState.ERROR,
    },
    RecoveryState.CONFIRMING_OFFLINE: {
        RecoveryEvent.CHECK_REQUESTED: RecoveryState.CHECKING,
        RecoveryEvent.STREAM_OFFLINE: RecoveryState.OFFLINE,
        RecoveryEvent.LIVE_DETECTED: RecoveryState.PREPARING,
        RecoveryEvent.RESOLVER_FAILED: RecoveryState.RECOVERING,
        RecoveryEvent.ROOM_DISABLED: RecoveryState.DISABLED,
        RecoveryEvent.MANUAL_STOP_REQUESTED: RecoveryState.STOPPING,
    },
    RecoveryState.CONVERTING: {
        RecoveryEvent.CONVERSION_SUCCEEDED: RecoveryState.CONFIRMING_OFFLINE,
        RecoveryEvent.CONVERSION_FAILED: RecoveryState.ERROR,
        RecoveryEvent.MANUAL_STOP_REQUESTED: RecoveryState.STOPPING,
        RecoveryEvent.PROTECTIVE_FAILURE: RecoveryState.ERROR,
        RecoveryEvent.ROOM_DISABLED: RecoveryState.DISABLED,
    },
    RecoveryState.OFFLINE: {
        RecoveryEvent.CHECK_REQUESTED: RecoveryState.CHECKING,
        RecoveryEvent.ROOM_ENABLED: RecoveryState.OFFLINE,
        RecoveryEvent.ROOM_DISABLED: RecoveryState.DISABLED,
        RecoveryEvent.LIVE_DETECTED: RecoveryState.PREPARING,
        RecoveryEvent.STREAM_OFFLINE: RecoveryState.OFFLINE,
        RecoveryEvent.RESOLVER_FAILED: RecoveryState.RECOVERING,
        RecoveryEvent.MANUAL_STOP_REQUESTED: RecoveryState.STOPPING,
        RecoveryEvent.PROTECTIVE_FAILURE: RecoveryState.ERROR,
    },
    RecoveryState.ERROR: {
        RecoveryEvent.CHECK_REQUESTED: RecoveryState.CHECKING,
        RecoveryEvent.ROOM_ENABLED: RecoveryState.OFFLINE,
        RecoveryEvent.ROOM_DISABLED: RecoveryState.DISABLED,
        RecoveryEvent.LIVE_DETECTED: RecoveryState.PREPARING,
        RecoveryEvent.STREAM_OFFLINE: RecoveryState.OFFLINE,
        RecoveryEvent.RESOLVER_FAILED: RecoveryState.RECOVERING,
        RecoveryEvent.MANUAL_STOP_REQUESTED: RecoveryState.STOPPING,
    },
    RecoveryState.STOPPING: {
        RecoveryEvent.STOP_COMPLETED: RecoveryState.OFFLINE,
        RecoveryEvent.PAUSE_COMPLETED: RecoveryState.DISABLED,
    },
    RecoveryState.DISABLED: {
        RecoveryEvent.ROOM_ENABLED: RecoveryState.OFFLINE,
        RecoveryEvent.STREAM_OFFLINE: RecoveryState.DISABLED,
    },
}


class RecoveryStateMachine:
    """A small, strict state machine for one room's runtime lifecycle."""

    def __init__(self, initial: RecoveryState = RecoveryState.IDLE) -> None:
        self._state = RecoveryState(initial)

    @property
    def state(self) -> RecoveryState:
        return self._state

    def can_transition(self, event: RecoveryEvent) -> bool:
        event = RecoveryEvent(event)
        return event in _TRANSITIONS[self._state]

    def transition(self, event: RecoveryEvent) -> RecoveryState:
        event = RecoveryEvent(event)
        try:
            next_state = _TRANSITIONS[self._state][event]
        except KeyError as error:
            raise InvalidRecoveryTransition(self._state, event) from error
        self._state = next_state
        return self._state


class RecoveryStateStore:
    """Keep one state machine per room and share it across monitor/recorder."""

    def __init__(self) -> None:
        self._machines: dict[str, RecoveryStateMachine] = {}

    def machine_for(self, room_id: str) -> RecoveryStateMachine:
        return self._machines.setdefault(room_id, RecoveryStateMachine())

    def state_for(self, room_id: str) -> RecoveryState:
        return self.machine_for(room_id).state

    def transition(self, room_id: str, event: RecoveryEvent) -> RecoveryState:
        return self.machine_for(room_id).transition(event)

    def discard(self, room_id: str) -> None:
        self._machines.pop(room_id, None)

