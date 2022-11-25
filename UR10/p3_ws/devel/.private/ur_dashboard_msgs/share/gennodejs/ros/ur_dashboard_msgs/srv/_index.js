
"use strict";

let IsInRemoteControl = require('./IsInRemoteControl.js')
let RawRequest = require('./RawRequest.js')
let IsProgramRunning = require('./IsProgramRunning.js')
let Popup = require('./Popup.js')
let GetProgramState = require('./GetProgramState.js')
let GetLoadedProgram = require('./GetLoadedProgram.js')
let AddToLog = require('./AddToLog.js')
let Load = require('./Load.js')
let GetRobotMode = require('./GetRobotMode.js')
let IsProgramSaved = require('./IsProgramSaved.js')
let GetSafetyMode = require('./GetSafetyMode.js')

module.exports = {
  IsInRemoteControl: IsInRemoteControl,
  RawRequest: RawRequest,
  IsProgramRunning: IsProgramRunning,
  Popup: Popup,
  GetProgramState: GetProgramState,
  GetLoadedProgram: GetLoadedProgram,
  AddToLog: AddToLog,
  Load: Load,
  GetRobotMode: GetRobotMode,
  IsProgramSaved: IsProgramSaved,
  GetSafetyMode: GetSafetyMode,
};
