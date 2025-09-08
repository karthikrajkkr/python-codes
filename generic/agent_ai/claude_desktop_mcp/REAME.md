
### Web Browser
- web-browser automation : https://github.com/microsoft/playwright-mcp


### MYSQL
- mysql mcp server : https://github.com/designcomputer/mysql_mcp_server
 
**pre-requisite:**
- Run commands to install the asked dependencies.
  ```
  pip install uv 
  # which/where gives the executable path to use in mcp server config
  which uv #linux
  where uv #windows
  
  
  pip install mysql-mcp-server
  pip show mysql-mcp-server # To get the path of pkg to use in mcp server config
  ```
- https://dev.mysql.com/downloads/installer/
- https://dev.mysql.com/downloads/workbench/

### Filesystem
- https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem


**Note**: 
- ```npx -y clear-npx-cache``` is to clear cache when you face npx issues.