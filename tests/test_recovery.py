import pytest

from reco_box.recovery import (
    InvalidRecoveryTransition,
    RecoveryEvent,
    RecoveryState,
    RecoveryStateMachine,
    RecoveryStateStore,
)


def test_recovery_state_machine_covers_live_retry_and_new_attempt() -> None:
    machine = RecoveryStateMachine()

    assert machine.transition(RecoveryEvent.CHECK_REQUESTED) is RecoveryState.CHECKING
    assert machine.transition(RecoveryEvent.LIVE_DETECTED) is RecoveryState.PREPARING
    assert machine.transition(RecoveryEvent.RECORDING_STARTED) is RecoveryState.RECORDING
    assert machine.transition(RecoveryEvent.RECORDING_FAILED) is RecoveryState.RECOVERING
    assert machine.transition(RecoveryEvent.CHECK_REQUESTED) is RecoveryState.CHECKING
    assert machine.transition(RecoveryEvent.LIVE_DETECTED) is RecoveryState.PREPARING
    assert machine.transition(RecoveryEvent.RECORDING_STARTED) is RecoveryState.RECORDING


def test_clean_end_requires_offline_confirmation_before_offline() -> None:
    machine = RecoveryStateMachine(RecoveryState.RECORDING)

    assert machine.transition(RecoveryEvent.RECORDING_FINISHED) is RecoveryState.CONFIRMING_OFFLINE
    assert machine.state is not RecoveryState.OFFLINE
    assert machine.transition(RecoveryEvent.STREAM_OFFLINE) is RecoveryState.OFFLINE


def test_manual_pause_has_a_distinct_stopping_boundary() -> None:
    machine = RecoveryStateMachine(RecoveryState.RECORDING)

    assert machine.transition(RecoveryEvent.MANUAL_STOP_REQUESTED) is RecoveryState.STOPPING
    assert machine.transition(RecoveryEvent.PAUSE_COMPLETED) is RecoveryState.DISABLED


def test_conversion_pause_has_a_distinct_stopping_boundary() -> None:
    machine = RecoveryStateMachine(RecoveryState.CONVERTING)

    assert machine.transition(RecoveryEvent.MANUAL_STOP_REQUESTED) is RecoveryState.STOPPING
    assert machine.transition(RecoveryEvent.PAUSE_COMPLETED) is RecoveryState.DISABLED


def test_invalid_transition_does_not_mutate_state() -> None:
    machine = RecoveryStateMachine(RecoveryState.OFFLINE)

    with pytest.raises(InvalidRecoveryTransition) as raised:
        machine.transition(RecoveryEvent.RECORDING_STARTED)

    assert raised.value.state is RecoveryState.OFFLINE
    assert raised.value.event is RecoveryEvent.RECORDING_STARTED
    assert machine.state is RecoveryState.OFFLINE


def test_state_store_keeps_room_lifecycles_independent() -> None:
    store = RecoveryStateStore()

    store.transition("first", RecoveryEvent.CHECK_REQUESTED)
    store.transition("second", RecoveryEvent.LIVE_DETECTED)

    assert store.state_for("first") is RecoveryState.CHECKING
    assert store.state_for("second") is RecoveryState.PREPARING
    store.discard("first")
    assert store.state_for("first") is RecoveryState.IDLE

