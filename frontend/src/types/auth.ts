// A context is a way to share data/state globally across components without manually passing props
export interface AuthContextType {
  accessToken: string | null;
  setAccessToken: (token: string | null) => void;
}
