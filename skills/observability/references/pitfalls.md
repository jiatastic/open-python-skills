# Observability Pitfalls

## Common Issues

- **Missing service name**: traces hard to find
- **High-cardinality attributes**: huge storage costs
- **Late instrumentation**: middleware created before configure

## Fix Patterns

- Set `service_name` at startup
- Keep attributes low-cardinality (IDs, not full payloads)
- Call `configure()` before creating clients
