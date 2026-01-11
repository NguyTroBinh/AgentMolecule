from mcp.server.fastmcp import FastMCP
from app.mcp.tools import analyze_molecule, check_filters

# Khoi tao MCP Server
mcp_server = FastMCP("Chemistry-RDKit-Server")

# Cong cu phan tich
@mcp_server.tool()
def compute_molecule_properties(smiles: str) -> str:
    """Tinh toan cac chi so hoa hoc tu SMILES."""
    results = analyze_molecule(smiles)
    return str(results)

# Kiem tra voi bo loc
@mcp_server.tool()
def screen_molecule(props_json: str, filters_json: str) -> str:
    """Kiem tra vi pham quy tac va cham diem."""
    import json
    props = json.loads(props_json)
    filters = json.loads(filters_json)
    result = check_filters(props, filters)
    return str(result)

if __name__ == "__main__":
    # Khoi chay server qua giao thuc stdio
    mcp_server.run()