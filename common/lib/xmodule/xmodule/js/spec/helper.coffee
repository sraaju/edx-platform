# Stub Youtube API
window.YT =
  PlayerState:
    UNSTARTED: -1
    ENDED: 0
    PLAYING: 1
    PAUSED: 2
    BUFFERING: 3
    CUED: 5

window.TYPES =
  'undefined'        : 'undefined'
  'number'           : 'number'
  'boolean'          : 'boolean'
  'string'           : 'string'
  '[object Function]': 'function'
  '[object RegExp]'  : 'regexp'
  '[object Array]'   : 'array'
  '[object Date]'    : 'date'
  '[object Error]'   : 'error'

window.TOSTRING = Object.prototype.toString
window.STATUS = window.YT.PlayerState

window.whatType = (o) ->
  TYPES[typeof o] || TYPES[TOSTRING.call(o)] || (o ? 'object' : 'null');

oldGetWithPrefix = window.jQuery.getWithPrefix

jasmine.stubbedCaption =
      end: [3120, 6270, 8490, 21620, 24920, 25750, 27900, 34380, 35550, 40250, 43470, 47630, 54760, 58010, 63550, 68370, 69620, 79740, 91900, 96440, 100690, 103629, 116970, 121070, 122850, 127700, 131710, 136370, 139920, 142970, 145150, 146220, 148100, 153490, 154920, 162920, 165680, 172450, 178310, 179550, 183130, 184820, 190900, 192720, 196800, 199230, 203470, 209150, 211930, 215950, 220880, 226390, 229180, 230750, 232090, 234710, 235810, 238030, 245790, 251210, 255320, 259500, 260260, 262230, 263480, 280935, 291270, 294320, 300360, 305340, 309095, 317660, 319320, 321360, 324530, 328890, 333420, 336130, 338860, 342274, 344240, 347300, 347720, 348750, 355460, 355710, 363570, 366930, 370230, 372810, 379030, 384420, 386650, 388980, 393390, 397060, 400600, 404550, 414800, 418360, 422180, 428180, 433800, 436640, 439900, 440970, 442880, 445000, 451320, 463470, 466760, 471200, 474390, 480350, 483545, 492380, 497170, 502980, 510310, 512159, 516159, 519549, 524840, 529340]
      start: [1180, 3120, 6270, 14910, 21620, 24920, 25750, 27900, 34380, 35550, 40250, 43470, 47630, 54760, 58010, 63550, 68370, 72400, 79740, 91900, 96440, 100690, 111780, 116970, 121070, 122850, 127700, 131710, 139390, 139920, 142970, 145150, 146220, 152260, 153490, 154920, 162920, 165680, 172450, 178310, 179550, 183130, 184820, 190900, 192720, 196800, 199230, 203470, 209150, 211930, 215950, 220880, 226390, 229180, 230750, 232090, 234710, 235810, 241390, 245790, 251210, 255320, 259500, 260260, 262230, 269660, 285700, 291270, 294320, 300360, 305340, 312350, 317660, 319320, 321360, 324530, 328890, 333420, 336130, 338860, 342274, 344240, 347300, 347720, 348750, 355460, 355710, 363570, 366930, 370230, 376670, 379030, 384420, 386650, 388980, 393390, 397060, 400600, 404550, 414800, 418360, 422180, 428180, 433800, 436640, 439900, 440970, 442880, 445000, 451320, 463470, 466760, 471200, 474390, 480350, 487670, 492380, 497170, 502980, 510310, 512159, 516159, 519549, 524840]
      text: ["MICHAEL CIMA: So let's do the first one here.", "Vacancies, where do they come from?", "Well, imagine a perfect crystal.", "Now we know at any temperature other than absolute zero there's enough", "energy going around that some atoms will have more energy", "than others, right?", "There's a distribution.", "If I plot energy here and number, these atoms in the crystal will have a", "distribution of energy.", "And some will have quite a bit of energy, just for a moment.", "Of course they give up the energy to the neighboring atom.", "So the energy sloshes around amongst all these atoms in such a way that the", "average energy is kT, but an individual atom, for a short period of", "time, may actually have quite a bit of energy.", "And so what may happen is you can have a situation where an atom right here", "has a sufficient energy that it can break its bonds and hop onto the", "surface of the crystal.", "Now in my drawing I've broken four bonds, and I've made another bond.", "So the net change is--", "well, it cost me three bonds and I got back--", "or four bonds, sorry, and I got back-- one bond energy.", "So the net change of around three bond energies.", "And so that's how these vacancies actually occur is that at any", "temperature above absolute zero they are in an intrinsic", "part of a pure material.", "In other words, you can't help at any temperature above absolute zero to", "have at least a few vacancies present.", "Even in a intrinsic material, one that's just a pure material.", "Why is that?", "Well, because there's enough energy to form them.", "So let's see how much--", "well let me show you.", "I got a little picture here.", "Here's a STM--", "Scanning Tunneling Microscope--", "image of the surface of a platinum crystal and a surface", "of a piece of silicon.", "Now if this is a vicinally-cut crystal so that it's not exactly coincident", "with one of the major planes, you can see though that the surface kind of", "corrugates like this.", "But you can see here, here, here, here, even at the", "surface there's an absence.", "You can see some of these individual vacancies that occur there.", "How was that vacancy created?", "Well the atom that was there just hopped out onto the surface, had", "sufficient energy to actually do that.", "Here is what we call a reconstructed (111) surface of silicon.", "If you actually look at the crystal structure in the (111) plane in the", "crystal structure of silicon, you don't actually see this pattern.", "Because what happens is these silicons on the surface want to satisfy their", "bonding so they actually bend at the surface to create more bonding.", "And so they create this new- I would call it new-- symmetry on the surface.", "But despite that you can see that it's not perfect.", "There are defects in here.", "There are individual absences.", "Now of course this is just on the surface, but the same", "is true in the bulk.", "You can actually see these atoms.", "So how many atoms will have sufficient energy?", "So the fraction of vacant sites is going to be the number of vacancies", "divided by total number of sites.", "And that's going to depend on an exponential function of", "temperature, right?", "It's sort of a Boltzmann factor.", "It is a Boltzmann factor.", "Where this is the energy required to make a vacancy.", "In other words, that would be roughly, in my sort of flat land world crystal", "up here, three bonds.", "Now if it was an FCC crystal like platinum here, and I'm going to take", "an atom inside this crystal and put it on the surface, I'm probably going to", "put it on a location where it can make how many bonds?", "If I put it on a close-packed surface, how many bonds will my new atom form?", "STUDENT: Four?", "MICHAEL CIMA: Three, right?", "Close-packed surface.", "Here's my surface like this.", "If I put an atom right down on this, I'll form three.", "It's got three nearest neighbors in the plane below.", "How many bonds did I break by pulling it out of the", "middle of an FCC crystal?", "STUDENT: [INAUDIBLE].", "MICHAEL CIMA: What's the coordination number for an atom in an FCC crystal?", "STUDENT: 12.", "MICHAEL CIMA: 12.", "So I had to break 12 bonds, and I get three back.", "Right?", "So this delta H of vacancies for the case of an FCC crystal is", "approximately 12 bond energies--", "I'll call it a b for bond energy--", "minus three that I get back.", "So now you can get the connection, right?", "If you can know the bond energy, you know how many bonds are formed in this", "crystal structure and how many you make by putting", "it back on the surface.", "You can use what you've learned about bond energies to predict what the heat", "of vacancy formation is.", "Well, let's do it for copper.", "I've sort of done it for us here.", "If you do that same calculation for copper, it's 1.03 eV per atom.", "I haven't told you what A is of this pre-exponential factor.", "It tends to be around 1.", "And in fact, if you're not given this you have two options.", "You either assume that it's 1, you have to assume that it's 1, or if you", "have it at two different temperatures, you have the vacancy concentration at", "two different temperatures, you don't need to assume it has", "a particular value.", "You can calculate it.", "But it generally is around 1.", "For copper, A turns out is 1.1.", "So if we do this calculation at room temperature, you get 2.19 times 10 to", "the minus 18.", "So that's the number of vacancies divided by the number of sites.", "So it's extremely small, right?", "If you work it out from the density of copper, this converts to about 1.8", "times 10 to the fifth per cubic centimeter.", "So it's about 20,000 vacancies per cubic centimeter.", "So it's a very small number, right?", "If you do it at the melting point of copper, you just apply these numbers", "at the melting point, which is 1085 centigrade, you get 1.67 times 10 to", "the minus fourth.", "So look at how many decades this changed.", "14 orders of magnitude.", "And that ends up being, on a volumetric basis, 1.41 times 10 to the", "19 per cubic centimeter."]

# For our purposes, we need to make sure that the function $.getWithPrefix doe not fail
# when during tests a captions file is requested. It is originally defined in
#
#     common/static/coffee/src/ajax_prefix.js
#
# We will replace it with a function that does:
#
#     1.) Return a hard coded captions object if the file name contains 'test_name_of_the_subtitles'.
#     2.) Behaves the same a as the origianl in all other cases.
window.jQuery.getWithPrefix = (url, data, callback, type) ->
  if url.match(/test_name_of_the_subtitles/g) isnt null or url.match(/slowerSpeedYoutubeId/g) isnt null or url.match(/normalSpeedYoutubeId/g) isnt null
    if window.jQuery.isFunction(callback) is true
      callback jasmine.stubbedCaption
    else if window.jQuery.isFunction(data) is true
      data jasmine.stubbedCaption
  else
    oldGetWithPrefix.apply this, arguments

# Time waitsFor() should wait for before failing a test.
window.WAIT_TIMEOUT = 1000

jasmine.getFixtures().fixturesPath = 'xmodule/js/fixtures'

jasmine.stubbedMetadata =
  slowerSpeedYoutubeId:
    id: 'slowerSpeedYoutubeId'
    duration: 300
  normalSpeedYoutubeId:
    id: 'normalSpeedYoutubeId'
    duration: 200
  bogus:
    duration: 100

jasmine.fireEvent = (el, eventName) ->
  if document.createEvent
    event = document.createEvent "HTMLEvents"
    event.initEvent eventName, true, true
  else
    event = document.createEventObject()
    event.eventType = eventName
  event.eventName = eventName
  if document.createEvent
    el.dispatchEvent(event)
  else
    el.fireEvent("on" + event.eventType, event)

jasmine.stubbedHtml5Speeds = ['0.75', '1.0', '1.25', '1.50']

jasmine.stubRequests = ->
  spyOn($, 'ajax').andCallFake (settings) ->
    if match = settings.url.match /youtube\.com\/.+\/videos\/(.+)\?v=2&alt=jsonc/
      settings.success data: jasmine.stubbedMetadata[match[1]]
    else if match = settings.url.match /static(\/.*)?\/subs\/(.+)\.srt\.sjson/
      settings.success jasmine.stubbedCaption
    else if settings.url.match /.+\/problem_get$/
      settings.success html: readFixtures('problem_content.html')
    else if settings.url == '/calculate' ||
      settings.url.match(/.+\/goto_position$/) ||
      settings.url.match(/event$/) ||
      settings.url.match(/.+\/problem_(check|reset|show|save)$/)
      # do nothing
    else
      throw "External request attempted for #{settings.url}, which is not defined."

jasmine.stubYoutubePlayer = ->
  YT.Player = ->
    obj = jasmine.createSpyObj 'YT.Player', ['cueVideoById', 'getVideoEmbedCode',
    'getCurrentTime', 'getPlayerState', 'getVolume', 'setVolume', 'loadVideoById',
    'playVideo', 'pauseVideo', 'seekTo', 'getDuration', 'getAvailablePlaybackRates', 'setPlaybackRate']
    obj['getAvailablePlaybackRates'] = jasmine.createSpy('getAvailablePlaybackRates').andReturn [0.75, 1.0, 1.25, 1.5]
    obj

jasmine.stubVideoPlayer = (context, enableParts, createPlayer=true) ->
  enableParts = [enableParts] unless $.isArray(enableParts)
  suite = context.suite
  currentPartName = suite.description while suite = suite.parentSuite
  enableParts.push currentPartName

  loadFixtures 'video.html'
  jasmine.stubRequests()
  YT.Player = undefined
  videosDefinition = '0.75:slowerSpeedYoutubeId,1.0:normalSpeedYoutubeId'
  context.video = new Video '#example', videosDefinition
  jasmine.stubYoutubePlayer()
  if createPlayer
    return new VideoPlayer(video: context.video)

jasmine.stubVideoPlayerAlpha = (context, enableParts, html5=false) ->
  console.log('stubVideoPlayerAlpha called')
  suite = context.suite
  currentPartName = suite.description while suite = suite.parentSuite
  if html5 == false
    loadFixtures 'videoalpha.html'
  else
    loadFixtures 'videoalpha_html5.html'
  jasmine.stubRequests()
  YT.Player = undefined
  window.OldVideoPlayerAlpha = undefined
  jasmine.stubYoutubePlayer()
  return new VideoAlpha '#example', '.75:slowerSpeedYoutubeId,1.0:normalSpeedYoutubeId'


# Stub jQuery.cookie
$.cookie = jasmine.createSpy('jQuery.cookie').andReturn '1.0'

# Stub jQuery.qtip
$.fn.qtip = jasmine.createSpy 'jQuery.qtip'

# Stub jQuery.scrollTo
$.fn.scrollTo = jasmine.createSpy 'jQuery.scrollTo'
