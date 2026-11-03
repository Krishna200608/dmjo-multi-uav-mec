import numpy as np

from src.buffer import RolloutBuffer


def test_rollout_buffer_batches_only_filled_steps():
    buffer = RolloutBuffer(
        rollout_length=5,
        n_agents=2,
        obs_dim=3,
        state_dim=4,
        action_dim=5,
    )

    for idx in range(2):
        buffer.insert(
            obs=np.full((2, 3), idx, dtype=np.float32),
            state=np.full(4, idx, dtype=np.float32),
            actions=np.zeros((2, 5), dtype=np.float32),
            log_probs=np.zeros(2, dtype=np.float32),
            rewards=np.ones(2, dtype=np.float32),
            done=0.0,
            values=np.zeros(2, dtype=np.float32),
        )

    buffer.compute_gae(last_values=np.zeros(2, dtype=np.float32), last_done=0.0)
    batches = list(buffer.get_batches(num_mini_batches=4))
    sample_count = sum(batch["obs"].shape[0] for batch in batches)

    assert buffer.step == 2
    assert sample_count == 4
    assert all(batch["obs"].shape[1] == 3 for batch in batches)
