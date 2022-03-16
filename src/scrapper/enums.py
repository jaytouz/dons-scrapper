class PoliticalEntitiesId:
    """
    tag id of the political entities checkbox

    """
    POLITICAL_PARTIES = "ckParti"
    INDEPENDANT_MEMBERS = "ckDIA"
    INDEPENDANT_CANDIDATES = "ckCIA"
    LEADERSHIP_RACE = "ckENT"


class DropdownClassName:
    """
     Class name of the dropdown related to the value types
    """
    YEARS = "multiSelect1"
    POLITICAL_PARTIES = "multiSelect2"
    INDEPENDANT_MEMBERS = "multiSelect3"
    INDEPENDANT_CANDIDATES = "multiSelect4"
    LEADERSHIP_RACE = "multiSelect5"
    LEADER = "multiSelect6"


class CheckboxClassName:
    """
    Class name of the dropdown related to the value types

    """
    YEARS = "multiSelectOptions1"
    POLITICAL_PARTIES = "multiSelectOptions2"
    INDEPENDANT_MEMBERS = "multiSelectOptions3"
    INDEPENDANT_CANDIDATES = "multiSelectOptions4"
    LEADERSHIP_RACE = "multiSelectOptions5"
    LEADER = "multiSelectOptions6"


class ValuesType:
    """Types of data that can be search in dropdowns"""
    YEAR = "years"
    MEMBERS = "members"
    PARTIES = "parties"
    CANDIDATES = "candidates"
    RACE = "leadership race"
    LEADER = "leaders"


class CheckboxValues(object):
    pass


class PoliticalPartiesValues(CheckboxValues):
    """Checkbox values in the dropdown menu of Parti Politique

    Make sure the values are correct before starting a new scrapping session
    """
    ADQ = "00049"  # Action démocratique du Québec (A.D.Q.)
    AQ = "00075"  # Affiliation Québec (A.Q.)
    APQ = "00105"  # Alliance provinciale du Québec (A.P.Q.)
    BES = "9994"  # Bloc équité sociale (B.É.S.)
    BP = "00059"  # Bloc pot (B.P.)
    CINQ = "00094"  # Changement intégrité pour notre Québec (C.I.N.Q.)
    CPQ = "00110"  # Citoyens au pouvoir du Québec (C.P.Q.)
    # Citoyens au pouvoir du Québec avant fusion avec P.Éq. (C.P.Q.)
    CPQ_PRE = "00089"
    CQ = "99237"  # Climat Québec (C.Q.)
    # Coalition avenir Québec (C.A.Q.) avant fusion avec l'A.D.Q.
    CAQ_EFL = "00084"
    # Coalition avenir Québec - L'équipe François Legault(C.A.Q.- É.F.L.)
    CAQ = "00085"
    DSD = "00108"  # Droit des sans droits (D.S.D.)
    EA = "00087"  # Équipe autonomiste (É.A.)
    MPQ = "00091"  # Mon pays le Québec (M.P.Q.)
    MEQ = "00077"  # Mouvement équité au Québec (M.E.Q.)
    NPDQ = "00092"  # Nouveau Parti démocratique du Québec (N.P.D.Q.)
    NAQC = "00081"  # Nouvelle Alliance Québec-Canada  (N.A.Q.C.)
    ON = "00083"  # Option nationale (O.N.)
    PAPE = "99236"  # Parti accès propriété et équité (P.A.P.É.)
    PAQ = "99224"  # Parti autochtone du Québec (P.A.Q.)
    PCQ = "00070"  # Parti communiste du Québec (P.C.Q.)
    PCU = "9998"  # Parti conscience universelle (P.C.U.)
    # Parti conservateur du Québec / Conservative Party of Québec (P.C.Q./C.P.Q.)
    PCQ_CPQ = "00079"
    PCuQ = "00106"  # Parti culinaire du Québec (P.Cu.Q.)
    PCMQ = "00088"  # Parti de la classe moyenne du Québec (P.C.M.Q.)
    PDS = "99910"  # Parti de la démocratie socialiste (P.D.S.)
    # Parti de la loi naturelle du Québec/Natural Law Party of Québec (P.L.N.Q./N.L.P.Q.)
    PLNQ = "99911"
    PDQ = "99913"  # Parti démocrate du Québec (P.D.Q.)
    PIQ = "99999"  # Parti des immigrés du Québec (P.I.Q.)
    PDQ2 = "99912"  # Parti durable du Québec (P.D.Q.)
    PE = "00052"  # Parti égalité/Equality Party (P.É./E.P.)
    PEq = "00086"  # Parti équitable (P.Éq)
    PI = "00073"  # Parti indépendantiste   (P.I.)
    PIQ = "99916"  # Parti innovateur du Québec (P.I.Q.)
    # Parti libéral du Québec/Quebec Liberal Party (P.L.Q./Q.L.P.)
    PLQ_QLP = "00010"
    PL = "00103"  # Parti libre (P.L.)
    PMLQ = "00034"  # Parti marxiste-léniniste du Québec (P.M.L.Q.)
    PN = "00080"  # Parti nul (P.N.)
    PIQ2 = "00113"  # Parti pour l'indépendance du Québec (P.I.Q.)
    PQ = "00016"  # Parti québécois (P.Q.)
    PRQ = "99921"  # Parti république du Québec (P.R.Q.)
    PRQ2 = "00111"  # Parti royaliste du Québec (P.R.Q.)
    PTQ = "00093"  # Parti travailliste du Québec (P.T.Q.)
    PUQ = "99922"  # Parti unitaire du Québec (P.U.Q.)
    PUN = "00063"  # Parti unité nationale (P.U.N.)
    # Parti vert du Québec/Green Party of Québec (P.V.Q./G.P.Q.)
    PVQ_GPQ = "00061"
    P51 = "00102"  # Parti 51 (P51)
    QRD = "00082"  # Québec - Révolution démocratique (Q.R.D.)
    QC_CQ = "00107"  # Québec cosmopolitain / Cosmpolitan Québec (Q.C./C.Q.)
    QM = "00104"  # Québec en marche (Q.M.)
    QS = "00039"  # Québec solidaire (Q.S.)
    QS_PRE = "00065"  # Québec solidaire avant fusion avec O.N (Q.S.)
    RAP = "99926"  # Rassemblement pour l'alternative progressiste (R.A.P.)
    # Union citoyenne du Québec / Québec Citizens' Union (U.C.Q./Q.C.U.)
    UCQ_QCU = "00090"
    UFP = "99927"  # Union des forces progressistes (U.F.P.)
    UC = "99928"  # Union du centre (U.C.)
    UN = "99209"  # Union nationale (U.N.)
    VP = "00109"  # Voie du peuple (V.P.)
    VQ = "99929"  # Votepop Québec (V.Q.)


class IndependantMembersValues(CheckboxValues):
    """Checkbox values in the dropdown menu of 'Depute independant'

    Make sure the values are correct before starting a new scrapping session
    """
    BENOIT_CHARETTE = "00096"  # Benoit Charette, DIA
    CATHERINE_FOURNIER = "00112"  # Catherine Fournier, DIA
    ERIC_CAIRE = "00099"  # Éric Caire, DIA
    FATIMA_HOUDE_PEPIN = "00100"  # Fatima Houda-Pepin , DIA
    GUY_OUELLETTE = "99215"  # Guy Ouellette, DIA
    LISETTE_LAPOINTE = "00097"  # Lisette Lapointe, DIA
    MARC_PICARD = "00098"  # Marc Picard, DIA
    PIERRE_CURZI = "00095"  # Pierre Curzi, DIA
    SYLVIE_ROY = "00101"  # Sylvie Roy, DIA


class IndependantCandidatesValues(CheckboxValues):
    """Checkbox values in the dropdown menu of 'Candidat independant'

    Make sure the values are correct before starting a new scrapping session
    """
    ALI_DAHAN = "18007"  # Ali Dahan, CIA
    ANTHONY_LECLERC = "12030"  # Anthony Leclerc, CIA
    BENOIT_ROY = "14002"  # Benoît Roy, CIA
    BERVERLY_BERNARDO = "18011"  # Berverly Bernardo, CIA
    CLAUDDE_ROY = "12006"  # Claude Roy, CIA
    CLAUDE_SURPRENANT = "18003"  # Claude Surprenant, CIA
    CYNTHIA_NICHOLS = "18008"  # Cynthia Nichols, CIA
    DENIS_BELANGER = "18006"  # Denis Bélanger, CIA
    DENIS_DURANT = "1009"  # Denis Durand, CIA
    ERIC_EMOND = "12008"  # Éric Émond, CIA
    FANG_HU = "18015"  # Fang Hu, CIA
    FRANCIS_JUNEAU = "12020"  # Francis Juneau, CIA
    FRANCOIS_XAVIER_RC = "17002"  # François-Xavier Richard-Choquette, CIA
    GILLES_ALARIE = "12014"  # Gilles Alarie, CIA
    GUY_GALLANT = "18004"  # Guy Gallant, CIA
    JEAN_MARIE_FN = "18012"  # Jean Marie Floriant Ndzana, CIA
    JEAN_MARC_BOYER = "18009"  # Jean-Marc Boyer, CIA
    JEAN_MARCEL_SECK = "12001"  # Jean-Marcel Seck, s'engage à se présenter CIA
    JEAN_MARK_BOYER = "14003"  # Jean-Mark Boyer, CIA
    JEAN_MATHIEU_DESMARAIS = "12011"  # Jean-Mathieu Desmarais, CIA
    JEAN_PIERRE_DUFAULT = "12024"  # Jean-Pierre Dufault, CIA
    JONATHAN_BEAULIEU = "18017"  # Jonathan Beaulieu-Richard, CIA
    JOSE_BRETON = "14001"  # José Breton, CIA
    LUC_LAINÉ = "18002"  # Luc Lainé, CIA
    LUTFI_KAMAL_G = "12043"  # Lutfi Kamal Germanos, CIA
    MARC_PETTERSEN = "14008"  # Marc Pettersen, CIA
    MARIE_PAULE_BERTRAND = "12004"  # Marie-Paule Bertrand, CIA
    MARIO_ROY = "14009"  # Mario Roy, CIA
    MARTIN_ROUSSEL = "12005"  # Martin Roussel, CIA
    MARTIN_ZIBEAU = "11001"  # Martin Zibeau, CIA
    MAXIM_SYLVESTRE = "18020"  # Maxim Sylvestre, CIA
    MICHEL_DUGRE = "12009"  # Michel Dugré, CIA
    PASCAL_TREMBLAY = "14004"  # Pascal Tremblay, CIA
    PATRIC_HAYES = "18014"  # Patrick Hayes, CIA
    PATRICK_TETREAULT = "18016"  # Patrick Tétreault, CIA
    REGENT_MILLETTE = "1008"  # Régent Millette, CIA
    ROBERT_GENESSE = "15001"  # Robert Genesse, CIA
    RODRIGUE_LEBLANC = "14005"  # Rodrigue Leblanc, CIA
    ROGER_DERY = "18019"  # Roger Déry, CIA
    ROGER_HUGHES = "14006"  # Roger Hughes, CIA
    SEBASTIEN_THEODORE = "17001"  # Sébastien Théodore, CIA
    SYLVAIN_LAROCQUE = "14007"  # Sylvain Larocque, CIA
    SYLVAIN_MARCOUX = "18010"  # Sylvain Marcoux, CIA
    TEODOR_DAIEV = "18018"  # Teodor Daiev, CIA
    VINCENT_BEGIN = "18013"  # Vincent Bégin, CIA
    VINCENT_BEGIN2 = "17003"  # Vincent Bégin, CIA
    WILLIAM_DUQUETTE = "18005"  # William Duquette, s'engage à se présenter CIA
    YVES_ST_DENIS = "18001"  # Yves St-Denis, CIA


class LeadershipRaceValues(CheckboxValues):
    """Checkbox values in the dropdown menu of 'Depute independant'

    Make sure the values are correct before starting a new scrapping session
    """
    PCQ_2021 = "21"  # P.C.Q-É.É.D. - 17 avril 2021
    PQ_2020 = "19"  # P.Q. - 9 octobre 2020
    PLQ_2020 = "18"  # P.L.Q./Q.L.P. - 31 mai 2020
    NPDQ_2018 = "17"  # N.P.D.Q. - 21 janvier 2018
    PQ_2016 = "14"  # P.Q. - 7 octobre 2016
    PQ_2015 = "11"  # P.Q. - 15 mai 2015
    ON_PIQ_2013 = "10"  # O.N. - P.I.Q. - 26 octobre 2013
    PVQ_2013 = "8"  # P.V.Q./G.P.Q. - 21 septembre 2013
    PLQ_2013 = "1"  # P.L.Q./Q.L.P. - 17 mars 2013
    PCQEED_2013 = "2"  # P.C.Q-É.É.D. - 24 février 2013
    EA_2013 = "3"  # É.A. - 19 janvier 2013


class LeadershipCandidateValues(CheckboxValues):
    """Checkbox values in the dropdown menu of 'Depute independant'

    Make sure the values are correct before starting a new scrapping session
    """
    ADRIEN_POULIOT = "5"  # Adrien D. Pouliot
    ALEX_TYRRELL = "12"  # Alex Tyrrell
    ALEXANDRE_CLOUTIER_15 = "27"  # Alexandre Cloutier 2015
    ALEXANDRE_CLOUTIER_16 = "33"  # Alexandre Cloutier2 2016
    ALEXANDRE_CUSSON = "47"  # Alexandre Cusson
    BERNARD_DRAINVILLE = "25"  # Bernard Drainville
    DANIEL_BRISSON_21 = "6"  # Daniel Brisson
    DANIEL_BRISSON_13 = "56"  # Daniel Brisson
    DOMINIQUE_ANGLADE = "46"  # Dominique Anglade
    ERIC_DUHAIME = "55"  # Éric Duhaime
    FREDERIC_BASTIEN = "49"  # Frédéric Bastien
    GLORIANE_BLAIS = "53"  # Gloriane Blais
    GUY_BOIVIN = "7"  # Guy Boivin
    GUY_NANTEL = "51"  # Guy Nantel
    JEAN_DAVID = "4"  # Jean David
    JEAN_CLAUDE_SA = "21"  # Jean-Claude St-André
    JEAN_F_LISEE_15 = "34"  # Jean-François Lisée 2015
    JEAN_F_LISEE_16 = "28"  # Jean-François Lisée 2016
    LAURENT_VEZINA = "52"  # Laurent Vézina
    LISA_JULIE_C = "14"  # Lisa Julie Cahn
    MARC_ANDRE_BEAUCHEMIN = "13"  # Marc-André Beauchemin
    MARTINE_OUELLET_15 = "36"  # Martine Ouellet 2015
    MARTINE_OUELLET_16 = "24"  # Martine Ouellet 2016
    NIC_PAYNE = "22"  # Nic Payne
    PATRICIA_DOMINGOS = "15"  # Patricia Domingos
    PATRICK_ST_ONGE = "57"  # Patrick St-Onge
    PAUL_SP_PLAMONDOND_16 = "37"  # Paul St-Pierre Plamondon 2016
    PAUL_SP_PLAMONDOND_20 = "50"  # Paul St-Pierre-Plamondon 2020
    PHILIPPE_COUILLARD = "1"  # Philippe Couillard
    PIERRE_CERE = "26"  # Pierre Céré
    PIERRE_KARL_PELADEAU = "29"  # Pierre Karl Péladeau
    PIERRE_MOREAU = "2"  # Pierre Moreau
    PIERRE_ETIENNE_LOIGNON = "20"  # Pierre-Etienne Loignon
    RAPHAEL_FORTIN = "44"  # Raphaël Fortin
    RAYMOND_BACHAND = "3"  # Raymond Bachand
    RAYMOND_COTE = "45"  # Raymond Côté
    SOL_ZENETTI = "23"  # Sol Zanetti
    SYLVAIN_GAUDREAULT = "48"  # Sylvain Gaudreault
    VERONIQUE_HIVON = "32"  # Véronique Hivon
