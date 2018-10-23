def print_differences(old, new, manual_ordered_keys=None, label=None):
    changed = False

    if not manual_ordered_keys:
        manual_ordered_keys = []

    seen_manual_ordered_keys = [False for key in manual_ordered_keys]

    keys = manual_ordered_keys + [
        key for key in sorted(list(new.keys()))
        if not manual_ordered_keys or key not in manual_ordered_keys
    ]

    for i, key in enumerate(keys):
        if key not in new:
            continue

        value = new[key]
        old_value = old.get(key)
        if value == old_value:
            continue

        if old_value is not None and old_value.__class__ != value.__class__:
            print(f'TYPE {key}: {old_value.__class__} -> {value.__class__}')
        # if not isinstance(value, str):
        #    print(f'RAW {key}: {old_value} -> {value}')

        if isinstance(value, list):
            value = set(value)
        if isinstance(old_value, list):
            old_value = set(old_value)
        if isinstance(value, str):
            value = value.strip()
        if isinstance(old_value, str):
            old_value = old_value.strip()

        if value == old_value:
            continue

        if label and not changed:
            print(f'Detected changes from {label}')

        changed = True
        if i <= len(manual_ordered_keys):
            if key in manual_ordered_keys:
                seen_manual_ordered_keys[i] = True

            # Show all previous values in manual_ordered_keys
            for prior_i in reversed(range(len(manual_ordered_keys))):
                if not seen_manual_ordered_keys[prior_i]:
                    context_key = manual_ordered_keys[prior_i]
                    context_value = new[context_key]
                    if context_value:
                        print(f'c.f. {context_key}: {context_value}')
                seen_manual_ordered_keys[prior_i] = True

        if not old_value:
            print(f'{key} (NEW): {value}')
            continue
        elif not value:
            print(f'{key} (DELETED): {old_value}')
            continue
        elif isinstance(value, set):
            if isinstance(old_value, str):
                print(f'{key} (TO SET): {old_value} -> {value}')
                continue
            elif not isinstance(old_value, set):
                print(f'{key} WTF {type(value)}: {old_value} -> {value}')
                continue
            if old_value > value:
                print(f'{key}: {sorted(old_value)} -'
                      f' {sorted(old_value - value)}')
            elif value > old_value:
                print(f'{key}: {sorted(old_value)} +'
                      f' {sorted(value - old_value)}')
            else:
                print(f'{key}: {sorted(old_value)} -> {sorted(value)}')
            continue
        elif not isinstance(value, str):
            print(f'{key}: {old_value} -> {value}')
            continue

        indent = ' ' * len(key)
        lines = set(value.splitlines())
        old_lines = set(old_value.splitlines())
        common_lines = lines.intersection(old_lines)
        if lines < old_lines:
            removed_lines = [line for line in old_lines.splitlines()
                             if line and line not in lines]
            print(f'{key} (REMOVED LINES):\n')
            for line in removed_lines:
                print(f'{indent} {line}')
            continue
        if lines > old_lines:
            new_lines = [line for line in value.splitlines()
                         if line and line not in old_lines]
            print(f'{key} (NEW LINES):\n')
            for line in new_lines:
                print(f'{indent} {line}')
            continue

        words = set(value.replace('\n', ' ').split(' '))
        old_words = set(old_value.replace('\n', ' ').split(' '))
        added = words - old_words
        removed = old_words - words
        if value.replace('\n', ' ') == old_value.replace('\n', ' '):
            print(f'{key} (EOL changes): {value}')
            continue
        elif not added and not removed:
            print(f'{key} (no changes??):\n'
                  f' - {old_value}\n + {value}')
            continue
        elif len(added) <= 3 and len(removed) <= 3:
            print(f'{key} (REMOVED): {sorted(removed)}\n'
                  f'{indent}     (NEW): {sorted(added)}')
            continue
        elif len(added) <= 3 and len(removed) <= 3:
            if removed:
                print(f'{key} (REMOVED): {sorted(removed)}')
            if remove and added:
                print(f'{indent}     (NEW): {sorted(added)}')
            else:
                print(f'{key} (NEW): {sorted(added)}')
            continue
        elif (len(lines) == len(old_lines) and
                len(common_lines) == len(lines) - 1):
            removed_line = list(old_lines - lines)[0]
            added_line = list(lines - old_lines)[0]
            print(f'{key}:\n'
                  f' - {removed_line}\n'
                  f' + {added_line}')
            continue

        print(f'{key} {-len(removed)} +{len(added)}:\n'
              f' - {old_value}\n'
              f' + {value}')

    return changed
