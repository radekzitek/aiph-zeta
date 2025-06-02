export interface User {
  username: string;
  email: string;
  first_name: string | null;
  last_name: string | null;
  is_active: boolean;
  is_superuser: boolean;
  id: string;
  created_at: string | null;
  updated_at: string | null;
  created_by: string | null;
  updated_by: string | null;
}
