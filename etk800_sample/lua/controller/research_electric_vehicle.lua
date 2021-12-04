-- This Source Code Form is subject to the terms of the bCDDL, v. 1.1.
-- If a copy of the bCDDL was not distributed with this
-- file, You can obtain one at http://beamng.com/bCDDL-1.1.txt

local M = {}
M.type = "auxiliary"
M.relevantDevice = nil

local function updateGFX(dt)
  --code here will be executed once each gfx frame, useful for logging data etc
end

local function init(jbeamData)
  --init stuff goes here
  print("I'm here")
end

M.init = init
M.updateGFX = updateGFX

return M
