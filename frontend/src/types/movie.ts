export interface Movie {
  title: string;
  tmdb_id: number;
  overview: string;
  poster_path?: string | null;
  release_year?: number | null;
  last_synced?: string;
}
