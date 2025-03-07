"// This is the main App component\n// This file defines the structure of the application\n// The App component serves as the root of the application\nimport Login from \"./components/Login\";\nimport Inventory from \"./components/Inventory\";\nimport UserRights from \"./components/UserRights\";\n\nfunction App() {\n  return (\n    <div>\n      <Navbar />\n      <Routes>\n        <Route path=\"/\" element={<Login />} />\n        <Route path=\"/inventory\" element={<Inventory />} />\n        <Route path=\"/user-rights\" element={<UserRights />} />\n      </Routes>\n    </div>\n  );\n}\n\nexport default App;"