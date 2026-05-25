# SKILL: Frontend Engineer — React/Vite/TypeScript
## Domain: React Frontend Development

**Activation triggers:** new page, component, hook, store, API integration,
routing, lazy loading, bundle optimization, TypeScript types.

---

## Component Template

```tsx
// pages/FeaturePage.tsx
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { expertApiClient } from '@/shared/api/client';

interface FeatureItem {
  id: string;
  name: string;
  is_active: boolean;
}

export default function FeaturePage() {
  const queryClient = useQueryClient();
  const [error, setError] = useState<string | null>(null);

  // Server state via React Query
  const { data: items = [], isLoading } = useQuery({
    queryKey: ['feature', 'items'],
    queryFn: () => expertApiClient.get<FeatureItem[]>('/api/v1/feature/items'),
    gcTime: 600_000,
    staleTime: 30_000,
  });

  // Mutations
  const createMutation = useMutation({
    mutationFn: (body: Partial<FeatureItem>) =>
      expertApiClient.post<FeatureItem>('/api/v1/feature/items', body),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['feature', 'items'] });
    },
    onError: (err: unknown) => {
      setError(err instanceof Error ? err.message : 'Failed');
    },
  });

  if (isLoading) return <LoadingFallback />;

  return (
    <div>
      {error && <ErrorMessage message={error} />}
      {items.map((item) => (
        <div key={item.id}>{item.name}</div>
      ))}
    </div>
  );
}
```

---

## State Management Rules

```typescript
// SERVER STATE → React Query (never store in Zustand)
useQuery({ queryKey: ['domain', 'resource'], queryFn: ... })

// GLOBAL UI STATE → Zustand with persist
const useDomainStore = create<DomainState>()(
  devtools(
    persist((set, get) => ({ ... }), { name: 'im-domain', version: 1 })
  )
)

// LOCAL UI STATE → useState / useReducer
const [isOpen, setIsOpen] = useState(false)

// FORM STATE → react-hook-form + zod
const form = useForm<FormData>({ resolver: zodResolver(schema) })
```

---

## API Client Rules

```typescript
// ALWAYS use typed clients — never raw fetch
import { expertApiClient, marketApiClient } from '@/shared/api/client';

// Expert backend (port 8002 in prod, Vite proxy in dev)
const accounts = await expertApiClient.get<BrokerAccount[]>('/api/v1/brokers/accounts');

// Market backend (port 8000 in prod, Vite proxy in dev)
const user = await marketApiClient.get<MeResponse>('/api/v1/auth/me');

// NEVER hardcode ports in components
// NEVER: fetch('http://localhost:8002/api/v1/...')
```

---

## Lazy Loading Pattern

```typescript
// ExpertRouter.tsx
const TradingJournalModule = lazy(() => import('./pages/TradingJournalModule'));
const CopyTradingPage = lazy(() => import('./pages/CopyTradingPage'));

export const ExpertRouter = () => (
  <Suspense fallback={<LoadingFallback />}>
    <Routes>
      <Route path="journal" element={<TradingJournalModule />} />
      <Route path="copy-trading" element={<CopyTradingPage />} />
    </Routes>
  </Suspense>
);
```

---

## TypeScript Rules

```typescript
// NEVER use `any`
function parseError(err: unknown): string {
  if (err instanceof ApiClientError) return err.message;
  if (err instanceof Error) return err.message;
  return String(err);
}

// Always type component props
interface AccountPillProps {
  onClick: () => void;
  compact?: boolean;
}
function AccountPill({ onClick, compact = false }: AccountPillProps) {}

// Type API responses
interface BrokerAccount {
  id: string;
  broker_type: string;
  account_name: string;
  display_name: string;   // normalized client-side
  is_active: boolean;
  is_default: boolean;
  last_balance: number | null;
}
```

---

## Anti-Patterns

```
✗ fetch() calls without error handling
✗ Server state in Zustand (use React Query)
✗ Missing TypeScript types (no `any`)
✗ useEffect for data fetching (use React Query)
✗ Prop drilling > 2 levels (use context or Zustand)
✗ Importing from another module's non-index files
✗ Hardcoded API base URLs
✗ Missing loading and error states in UI
✗ console.log left in production code
```
