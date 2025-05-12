class PixeldojoMcp < Formula
  include Language::Python::Virtualenv

  desc "MCP server for PixelDojo AI image generation API"
  homepage "https://github.com/mariusSil/pixeldojo-mcp-server"
  url "https://github.com/mariusSil/pixeldojo-mcp-server/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "PLACEHOLDER_SHA256_CHECKSUM" # Will be replaced with actual checksum after release
  license "MIT"

  depends_on "python@3.11"

  # Main dependencies
  resource "aiohttp" do
    url "https://files.pythonhosted.org/packages/d6/12/96982e7a7c09dc47c5e9ea9d4eaba3e9dbc62a5453cb491e5eb31a6c9a66/aiohttp-3.9.5.tar.gz"
    sha256 "02271f722e7a1f965cef05cb502ae5981c51a9d5e41dfc39a1bac1c276d52220"
  end

  resource "pydantic" do
    url "https://files.pythonhosted.org/packages/1b/1c/8c7720af1421ca05eeea4e71a5b32ea481aebd712e8548c9b3d5cb306b37/pydantic-2.7.0.tar.gz"
    sha256 "3ce13a558736b0804223a82499ad3848d9367561932876aaef98d5be6d2ab211"
  end

  resource "mcp" do
    url "https://files.pythonhosted.org/packages/d4/91/95f59c0af4c1fe9c10882cffc46fbff1f5c856a37a47e86adaea79c80d7a/mcp-1.8.0.tar.gz"
    sha256 "2d6775a3a9f57d4e0e0a88d48e7a5baaf62f0c78c10857d92cd63cb12a15c86c"
  end

  # Add additional Python package dependencies following the same pattern

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "pixeldojo-mcp", shell_output("#{bin}/pixeldojo-mcp --help", 2)
  end
end
