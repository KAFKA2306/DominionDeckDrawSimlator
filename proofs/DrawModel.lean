import Init

/-!
# Draw-model invariants

This models only the deterministic card-processing step used by
`probability.js`. A card consumes one available action and grants
`draw` additional actions; there is no reshuffle or action limit.

These proofs do NOT establish equivalence with JavaScript, correctness
of the probability-weighted dynamic program, or browser behavior.
-/

namespace DrawModel

/-- Whether a deck in a *fixed order* can be processed in its entirety. -/
def completes : List Nat → Nat → Bool
  | [], _ => true
  | _ :: _, 0 => false
  | draw :: rest, Nat.succ available =>
      completes rest (available + draw)

theorem empty_deck_succeeds (available : Nat) :
    completes [] available = true := rfl

theorem no_available_action_fails (draw : Nat) (rest : List Nat) :
    completes (draw :: rest) 0 = false := rfl

/-- A deck can always be fully processed if the initial available actions
    already cover all the cards, regardless of their draw values or order. -/
theorem enough_actions_always_complete
    (cards : List Nat) (available : Nat)
    (h : cards.length ≤ available) :
    completes cards available = true := by
  induction cards generalizing available with
  | nil =>
      rfl
  | cons draw rest ih =>
      cases available with
      | zero =>
          simp at h
      | succ usable =>
          have hlen : rest.length ≤ usable :=
            Nat.le_of_succ_le_succ h
          have hnext : rest.length ≤ usable + draw :=
            Nat.le_trans hlen (Nat.le_add_right usable draw)
          simpa [completes] using ih (usable + draw) hnext

/-- The early return for decks of size at most the five-card initial hand
    is valid for every ordering under this simplified draw model. -/
theorem five_cards_always_complete (cards : List Nat)
    (h : cards.length ≤ 5) : completes cards 5 = true :=
  enough_actions_always_complete cards 5 h

end DrawModel
