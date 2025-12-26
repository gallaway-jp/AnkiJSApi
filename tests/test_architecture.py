"""
Architectural tests for the AnkiDroid JS API.

These tests validate architectural rules and constraints to prevent
degradation over time. They ensure:
- No circular dependencies
- Layer isolation (feature modules don't depend on each other)
- Security module independence
- Module coupling stays within acceptable limits
"""

import ast
import os
from pathlib import Path
from typing import Set, Dict, List


def get_src_path() -> Path:
    """Get the path to the src directory."""
    # Go up from tests/ to project root, then to src/
    test_dir = Path(__file__).parent
    project_root = test_dir.parent
    return project_root / "src" / "ankidroid_js_api"


def parse_imports(file_path: Path) -> Set[str]:
    """Parse Python file and extract all import statements.
    
    Args:
        file_path: Path to Python file
        
    Returns:
        Set of module names imported (relative to ankidroid_js_api)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read(), filename=str(file_path))
        except SyntaxError:
            return set()
    
    imports = set()
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                if node.module.startswith('.'):
                    # Relative import within package (e.g., "from . import card_info")
                    module = node.module.lstrip('.')
                    if module:  # "from .module import"
                        imports.add(module.split('.')[0])
                    else:
                        # "from . import module" - get names
                        for alias in node.names:
                            imports.add(alias.name.split('.')[0])
                else:
                    # Absolute import
                    imports.add(node.module.split('.')[0])
            else:
                # "from . import x, y, z"
                for alias in node.names:
                    imports.add(alias.name.split('.')[0])
    
    return imports


def build_dependency_graph() -> Dict[str, Set[str]]:
    """Build a dependency graph of all modules.
    
    Returns:
        Dictionary mapping module name to set of modules it imports
    """
    src_path = get_src_path()
    graph = {}
    
    # Get all Python files
    for py_file in src_path.glob("*.py"):
        if py_file.name == "__init__.py":
            continue
        
        module_name = py_file.stem
        imports = parse_imports(py_file)
        
        # Filter to only our modules
        our_modules = {
            'security', 'utils', 'constants', 'card_info', 'card_actions',
            'reviewer_control', 'tts_control', 'ui_control', 'tag_manager',
            'api_bridge', 'tts_strategies'
        }
        
        filtered_imports = imports & our_modules
        graph[module_name] = filtered_imports
    
    return graph


def find_cycles(graph: Dict[str, Set[str]]) -> List[List[str]]:
    """Find all cycles in the dependency graph using DFS.
    
    Args:
        graph: Dependency graph
        
    Returns:
        List of cycles (each cycle is a list of module names)
    """
    def dfs(node: str, path: List[str], visited: Set[str], rec_stack: Set[str]) -> List[List[str]]:
        visited.add(node)
        rec_stack.add(node)
        cycles = []
        
        for neighbor in graph.get(node, set()):
            if neighbor == node:
                # Self-reference, skip (not a real cycle)
                continue
            if neighbor not in visited:
                cycles.extend(dfs(neighbor, path + [node], visited, rec_stack))
            elif neighbor in rec_stack:
                # Found a cycle
                cycle_start = path.index(neighbor) if neighbor in path else len(path)
                cycle = path[cycle_start:] + [neighbor]
                # Only add if it's a real cycle (length > 1)
                if len(set(cycle)) > 1:
                    cycles.append(cycle)
        
        rec_stack.remove(node)
        return cycles
    
    visited = set()
    all_cycles = []
    
    for node in graph:
        if node not in visited:
            all_cycles.extend(dfs(node, [], visited, set()))
    
    return all_cycles


def test_no_circular_dependencies():
    """Ensure there are no circular dependencies between modules."""
    graph = build_dependency_graph()
    cycles = find_cycles(graph)
    
    assert len(cycles) == 0, f"Found circular dependencies: {cycles}"


def test_feature_module_isolation():
    """Ensure feature modules don't import from each other.
    
    Feature modules should only depend on infrastructure modules
    (utils, security, constants, tts_strategies).
    
    Exception: card_info provides get_current_card() which is a shared
    utility used by other feature modules.
    """
    feature_modules = {
        'card_actions', 'reviewer_control',
        'tts_control', 'ui_control', 'tag_manager'
    }
    
    graph = build_dependency_graph()
    
    violations = []
    for module in feature_modules:
        imports = graph.get(module, set())
        # card_info is allowed (provides get_current_card utility)
        feature_imports = imports & (feature_modules | {'card_info'}) - {'card_info'}
        
        if feature_imports:
            violations.append(f"{module} imports from feature module(s): {feature_imports}")
    
    assert len(violations) == 0, f"Feature module isolation violated:\n" + "\n".join(violations)


def test_security_module_independence():
    """Ensure security module doesn't depend on feature modules.
    
    The security module is a cross-cutting concern and should only
    depend on constants (or standard library).
    """
    graph = build_dependency_graph()
    security_imports = graph.get('security', set())
    
    # Security should only import from constants or nothing
    allowed_imports = {'constants'}
    forbidden_imports = security_imports - allowed_imports
    
    assert len(forbidden_imports) == 0, \
        f"Security module has forbidden dependencies: {forbidden_imports}"


def test_constants_independence():
    """Ensure constants module has no dependencies.
    
    Constants should be a leaf module with zero dependencies on other
    project modules (except internal sub-modules in constants package).
    """
    # Check if it's a package now
    src_path = get_src_path()
    constants_path = src_path / "constants"
    
    if constants_path.is_dir():
        # New package structure - check individual modules, not __init__.py
        # __init__.py can import from sub-modules (security, cards, tts, ui)
        for py_file in constants_path.glob("*.py"):
            if py_file.name in ("__init__.py", "__pycache__"):
                continue
            
            imports = parse_imports(py_file)
            our_modules = {
                'security', 'utils', 'card_info', 'card_actions',
                'reviewer_control', 'tts_control', 'ui_control', 'tag_manager',
                'api_bridge', 'tts_strategies', 'constants'
            }
            external_imports = imports & our_modules
            
            assert len(external_imports) == 0, \
                f"Constants sub-module {py_file.name} has external dependencies: {external_imports}"
    else:
        # Old single file structure
        graph = build_dependency_graph()
        constants_imports = graph.get('constants', set())
        
        assert len(constants_imports) == 0, \
            f"Constants module should have no dependencies, found: {constants_imports}"


def test_utils_limited_dependencies():
    """Ensure utils module has minimal dependencies.
    
    Utils should only depend on constants and security (for validation decorators).
    Exception: card_info is imported for get_current_card in decorators.
    """
    graph = build_dependency_graph()
    utils_imports = graph.get('utils', set())
    
    # Utils can import from security, constants, and card_info (for decorators)
    allowed_imports = {'security', 'constants', 'card_info'}
    forbidden_imports = utils_imports - allowed_imports
    
    assert len(forbidden_imports) == 0, \
        f"Utils module has forbidden dependencies: {forbidden_imports}"


def test_api_bridge_as_facade():
    """Ensure api_bridge imports all feature modules (facade pattern).
    
    api_bridge should be the central coordination point that knows
    about all feature modules.
    """
    graph = build_dependency_graph()
    bridge_imports = graph.get('api_bridge', set())
    
    expected_feature_imports = {
        'card_info', 'card_actions', 'reviewer_control',
        'tts_control', 'ui_control', 'tag_manager'
    }
    
    missing_imports = expected_feature_imports - bridge_imports
    
    assert len(missing_imports) == 0, \
        f"api_bridge should import all feature modules, missing: {missing_imports}"


def test_reasonable_coupling():
    """Ensure no module has excessive dependencies.
    
    A module importing more than 6 other project modules likely
    has too many responsibilities.
    
    Exception: api_bridge as facade can import from all feature modules.
    """
    graph = build_dependency_graph()
    max_dependencies = 6
    
    violations = []
    for module, imports in graph.items():
        # api_bridge is allowed to have many dependencies (it's the facade)
        if module == 'api_bridge':
            continue
            
        if len(imports) > max_dependencies:
            violations.append(f"{module} has {len(imports)} dependencies: {imports}")
    
    assert len(violations) == 0, \
        f"Modules with excessive coupling:\n" + "\n".join(violations)


def test_layer_hierarchy():
    """Ensure proper layer hierarchy is maintained.
    
    Layers (from bottom to top):
    1. Constants (no dependencies)
    2. Security (depends on constants only)
    3. card_info, Utils (can depend on each other - utils needs get_current_card, card_info needs decorators)
    4. Strategies (tts_strategies - depends on security, constants)
    5. Feature modules (depend on layers 1-4, and card_info)
    6. API Bridge (depends on all feature modules)
    """
    graph = build_dependency_graph()
    
    # Layer 1: Constants (checked in test_constants_independence)
    
    # Layer 2: Security
    security_imports = graph.get('security', set())
    allowed = {'constants'}
    forbidden = security_imports - allowed
    assert len(forbidden) == 0, \
        f"Layer 2 module security has forbidden dependencies: {forbidden}"
    
    # Layer 3: card_info, Utils (can reference each other)
    layer3_modules = {'card_info', 'utils'}
    for module in layer3_modules:
        imports = graph.get(module, set())
        # Can depend on constants, security, and each other
        allowed = {'constants', 'security', 'card_info', 'utils'}
        
        forbidden = imports - allowed
        assert len(forbidden) == 0, \
            f"Layer 3 module {module} has forbidden dependencies: {forbidden}"
    
    # Layer 4: Strategies
    layer4_modules = {'tts_strategies'}
    for module in layer4_modules:
        imports = graph.get(module, set())
        # Can depend on layers 1-2
        allowed = {'constants', 'security', 'utils'}
        forbidden = imports - allowed
        assert len(forbidden) == 0, \
            f"Layer 4 module {module} has forbidden dependencies: {forbidden}"
    
    # Layer 5: Feature modules (tested in test_feature_module_isolation)
    
    # Layer 6: API Bridge
    bridge_imports = graph.get('api_bridge', set())
    # Bridge can import from anywhere except other bridges (there's only one)
    # This is OK - it's the top layer


def test_module_count_reasonable():
    """Ensure the number of modules stays within reasonable limits.
    
    Too many modules (>20) suggests over-fragmentation.
    Too few modules (<8) suggests under-organization.
    """
    graph = build_dependency_graph()
    module_count = len(graph)
    
    assert 8 <= module_count <= 20, \
        f"Module count ({module_count}) outside reasonable range [8, 20]"


if __name__ == "__main__":
    # Run all tests
    import sys
    
    tests = [
        ("No circular dependencies", test_no_circular_dependencies),
        ("Feature module isolation", test_feature_module_isolation),
        ("Security module independence", test_security_module_independence),
        ("Constants independence", test_constants_independence),
        ("Utils limited dependencies", test_utils_limited_dependencies),
        ("API bridge as facade", test_api_bridge_as_facade),
        ("Reasonable coupling", test_reasonable_coupling),
        ("Layer hierarchy", test_layer_hierarchy),
        ("Module count reasonable", test_module_count_reasonable),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"✓ {name}")
            passed += 1
        except AssertionError as e:
            print(f"✗ {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {name}: Unexpected error: {e}")
            failed += 1
    
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
