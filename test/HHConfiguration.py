
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras
from cp3_llbb.Framework import Framework
from cp3_llbb.Framework import METProducer
from cp3_llbb.Framework.CmdLine import CmdLine

options = CmdLine()
runOnData = options.runOnData == 1

globalTag_ = '80X_mcRun2_asymptotic_2016_TrancheIV_v7'
processName_ = 'PAT'
if runOnData :
    globalTag_ = '80X_dataRun2_2016SeptRepro_v6'
    processName_ = 'RECO'

framework = Framework.Framework(runOnData, eras.Run2_25ns, globalTag=globalTag_, processName=processName_)

framework.addAnalyzer('hh_analyzer', cms.PSet(
        type = cms.string('hh_analyzer'),
        prefix = cms.string('hh_'),
        enable = cms.bool(True),
        categories_parameters = cms.PSet(
            # Per-category lepton pt cuts
            mumu_leadingLeptonPtCut = cms.untracked.double(20), # muon
            mumu_subleadingLeptonPtCut = cms.untracked.double(10), # muon
            elel_leadingLeptonPtCut = cms.untracked.double(25), # electron
            elel_subleadingLeptonPtCut = cms.untracked.double(15), # electron
            muel_leadingLeptonPtCut = cms.untracked.double(25), # muon
            muel_subleadingLeptonPtCut = cms.untracked.double(15), # electron
            elmu_leadingLeptonPtCut = cms.untracked.double(25), # electron
            elmu_subleadingLeptonPtCut = cms.untracked.double(10), # muon
        ),
        parameters = cms.PSet(
            # Producers
            electronsProducer = cms.string('electrons'),
            muonsProducer = cms.string('muons'),
            jetsProducer = cms.string('jets'),
            metProducer = cms.string('met'),
            nohfMETProducer = cms.string('nohf_met'),

            # Pre-selection pt cut, applied to all leptons
            leadingElectronPtCut = cms.untracked.double(25),
            subleadingElectronPtCut = cms.untracked.double(15),
            leadingMuonPtCut = cms.untracked.double(20),
            subleadingMuonPtCut = cms.untracked.double(10),

            electronEtaCut = cms.untracked.double(2.5),
            muonLooseIsoCut = cms.untracked.double(.25), # https://twiki.cern.ch/twiki/bin/view/CMS/TopMUO 
            muonTightIsoCut = cms.untracked.double(.15), # https://twiki.cern.ch/twiki/bin/view/CMS/TopMUO 
            muonEtaCut = cms.untracked.double(2.4),
            electrons_loose_wp_name = cms.untracked.string("cutBasedElectronID-Summer16-80X-V1-loose"),
            electrons_medium_wp_name = cms.untracked.string("cutBasedElectronID-Summer16-80X-V1-medium"),
            electrons_tight_wp_name = cms.untracked.string("cutBasedElectronID-Summer16-80X-V1-tight"),
            electrons_hlt_safe_wp_name = cms.untracked.string("cutBasedElectronHLTPreselection-Summer16-V1"),
            jetEtaCut = cms.untracked.double(2.4),
            jetPtCut = cms.untracked.double(20),

            # BTAG INFO
            # Working points from https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80XReReco
            discr_name =  cms.untracked.string("pfCombinedMVAV2BJetTags"),
            discr_cut_loose =  cms.untracked.double(-0.5884),
            discr_cut_medium =  cms.untracked.double(0.4432),
            discr_cut_tight =  cms.untracked.double(0.9432),

            minDR_l_j_Cut = cms.untracked.double(0.3),
            hltDRCut = cms.untracked.double(0.1),
            hltDPtCut = cms.untracked.double(0.5),  # cut will be DPt/Pt < hltDPtCut
            applyBJetRegression = cms.untracked.bool(False), # BE SURE TO ACTIVATE computeRegression FLAG BELOW

            hlt_efficiencies = cms.untracked.PSet(

                    IsoMu17leg = cms.untracked.FileInPath('cp3_llbb/Framework/data/Efficiencies/Muon_DoubleMu_IsoMu17leg_Run2016_PTvsETA_Run271036to276811_HWW_weighted.json'),
                    IsoMu8orIsoTkMu8leg = cms.untracked.FileInPath('cp3_llbb/Framework/data/Efficiencies/Muon_DoubleMu_IsoMu8orIsoTkMu8leg_Run2016_PTvsETA_Run271036to276811_HWW_weighted.json'),

                    DoubleEleHighPtleg = cms.untracked.FileInPath('cp3_llbb/Framework/data/Efficiencies/Electron_HLT_DoubleEleLegHigPt_HWW.json'),
                    DoubleEleLowPtleg = cms.untracked.FileInPath('cp3_llbb/Framework/data/Efficiencies/Electron_HLT_DoubleEleLegLowPt_HWW.json'),

                    EleMuHighPtleg = cms.untracked.FileInPath('cp3_llbb/Framework/data/Efficiencies/Electron_HLT_EleMuLegHigPt_HWW.json'),
                    MuEleLowPtleg = cms.untracked.FileInPath('cp3_llbb/Framework/data/Efficiencies/Electron_HLT_MuEleLegLowPt_HWW.json'),

                    IsoMu8leg = cms.untracked.FileInPath('cp3_llbb/Framework/data/Efficiencies/Muon_DoubleMu_IsoMu8leg_Run2016_PTvsETA_Run271036to276811_HWW_weighted.json'),
                    IsoMu23leg = cms.untracked.FileInPath('cp3_llbb/Framework/data/Efficiencies/Muon_DoubleMu_IsoMu23leg_Run2016_PTvsETA_Run271036to276811_HWW_weighted.json'),
            )
        )
    )
)

# Add PUPPI MET
puppiCfg = cms.PSet(METProducer.default_configuration.clone())
puppiCfg.prefix = cms.string('puppimet_')
puppiCfg.parameters.met = cms.untracked.InputTag('slimmedMETsPuppi')
framework.addProducer('puppimet', puppiCfg)

# Remove fat jets
framework.removeProducer('fat_jets')

framework.getProducer('hlt').parameters.triggers = cms.untracked.FileInPath('cp3_llbb/HHAnalysis/data/triggers.xml')
#framework.getProducer('jets').parameters.cut = cms.untracked.string("pt > 20")
#framework.getProducer('jets').parameters.computeRegression = cms.untracked.bool(True)

framework.redoJEC()
framework.smearJets()
framework.doSystematics(['jec', 'jer'])
process = framework.create()

if runOnData : 
    process.source.fileNames = cms.untracked.vstring(
        '/store/data/Run2016B/DoubleMuon/MINIAOD/PromptReco-v2/000/273/158/00000/A6AC80E5-121A-E611-A689-02163E01439E.root'
#        '/store/data/Run2016B/DoubleEG/MINIAOD/PromptReco-v2/000/274/442/00000/30D4864F-DD2D-E611-BDF9-02163E013427.root'
#        '/store/data/Run2016B/MuonEG/MINIAOD/PromptReco-v2/000/275/370/00000/2E773576-D938-E611-9FCE-02163E013753.root'
        )
else : 
    process.source.fileNames = cms.untracked.vstring(
        '/store/mc/RunIISpring16MiniAODv2/GluGluToRadionToHHTo2B2VTo2L2Nu_M-450_narrow_13TeV-madgraph/MINIAODSIM/PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/10000/702A12BA-1B3B-E611-9A14-0025907B4EC0.root'
#        '/store/mc/RunIISpring16MiniAODv2/TTTo2L2Nu_13TeV-powheg/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/60000/022B4AD3-7A1B-E611-812B-28924A33B9AA.root'
        )

#process.MessageLogger.cerr.FwkReport.reportEvery = 1
#process.source.skipEvents = cms.untracked.uint32(10)
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1000))
