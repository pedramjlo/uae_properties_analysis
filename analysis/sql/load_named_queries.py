def load_named_queries(path):
    with open(path) as f:
        content = f.read()

    queries = {}
    current_name = None
    current_query = []

    for line in content.splitlines():
        if line.strip().startswith("-- name:"):
            if current_name and current_query:
                queries[current_name] = "\n".join(current_query).strip()
            current_name = line.split(":", 1)[1].strip()
            current_query = []
        else:
            current_query.append(line)
    if current_name and current_query:
        queries[current_name] = "\n".join(current_query).strip()

    return queries
