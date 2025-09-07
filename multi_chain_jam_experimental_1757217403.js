// Multi-Chain Jam Session - Experimental
// Generated: 2025-09-07T05:56:43.663178
// Ethereum: Lead & Harmony | Bitcoin: Bass & Rhythm | Polygon: Percussion & Texture

setcps(1.70)

stack(
  // 🥁 COLLABORATIVE RHYTHM SECTION
  // Ethereum provides the main beat
  s("bd ~ bd").gain(0.8).room(0.2),
  
  // Bitcoin adds snare variations
  s("~ sd ~").gain(0.6).room(0.3),
  
  // Polygon adds hihat complexity
  s("hh*2").gain(0.4).room(0.1),
  
  // 🎹 ETHEREUM - Lead Melody & Harmony
  n("<60 62 63 65>")
  .scale("B:minor")
  .s("gm_lead_6_voice")
  .clip(perlin.range(0.1, 1.0).slow(2))
  .jux(rev)
  .room(0.8)
  .lpf(rand.range(400, 16000).slow(6))
  .gain(0.7),
  
  // 🎸 BITCOIN - Bass Foundation
  n("0 2 3 5")
  .scale("B:minor")
  .s("gm_acoustic_bass")
  .gain(0.6)
  .lpf(400)
  .room(0.4),
  
  // 🎛️ POLYGON - Percussion & Texture
  n("0 2 3 5")
  .scale("B:minor")
  .s("gm_synth_pad_2_warm")
  .gain(0.3)
  .room(0.6)
  .shape(0.4)
  .delay(0.1)
  .lpf(cosine.range(250, 14000).slow(4)),
  
  // 🎼 COLLABORATIVE HARMONIC LAYER
  // All chains contribute to the harmony
  n("0 2 3 5")
  .scale("B:minor")
  .s("gm_synth_strings_2")
  .gain(0.2)
  .room(0.8)
  .shape(0.3)
  .delay(0.05)
  
  // 🎵 INTERACTIVE ELEMENTS
  // Chains respond to each other
  .mask("<0 1 1 0>/8")  // Ethereum leads
  .mask("<1 0 0 1>/8")  // Bitcoin responds
  .mask("<0 0 1 1>/8")  // Polygon adds texture
)
.late("[0 .01]*2")
.size(2.5)