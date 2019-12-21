
"use strict";

let SetComplianceSlope = require('./SetComplianceSlope.js')
let RestartController = require('./RestartController.js')
let StopController = require('./StopController.js')
let StartController = require('./StartController.js')
let SetTorqueLimit = require('./SetTorqueLimit.js')
let SetCompliancePunch = require('./SetCompliancePunch.js')
let SetComplianceMargin = require('./SetComplianceMargin.js')
let SetSpeed = require('./SetSpeed.js')
let TorqueEnable = require('./TorqueEnable.js')

module.exports = {
  SetComplianceSlope: SetComplianceSlope,
  RestartController: RestartController,
  StopController: StopController,
  StartController: StartController,
  SetTorqueLimit: SetTorqueLimit,
  SetCompliancePunch: SetCompliancePunch,
  SetComplianceMargin: SetComplianceMargin,
  SetSpeed: SetSpeed,
  TorqueEnable: TorqueEnable,
};
