import { useEffect, useSyncExternalStore } from "react";

export type Role = "patient" | "clinician";

let role: Role = "patient";
const listeners = new Set<() => void>();

export function setRole(next: Role) {
  role = next;
  if (typeof document !== "undefined") {
    document.documentElement.dataset["role"] = next;
  }
  listeners.forEach((l) => l());
}

function subscribe(l: () => void) {
  listeners.add(l);
  return () => listeners.delete(l);
}

export function useRole(): Role {
  const value = useSyncExternalStore(
    subscribe,
    () => role,
    () => "patient" as Role,
  );
  useEffect(() => {
    document.documentElement.dataset["role"] = role;
  }, [value]);
  return value;
}
