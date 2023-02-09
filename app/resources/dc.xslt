<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:meemoo="https://data.hetarchief.be/ns/algemeen#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:schema="http://schema.org/" xmlns:ebu="urn:ebu:metadata-schema:ebuCore_2012" xmlns:ebucore="urn:ebu:metadata-schema:ebucore" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:viaa="http://www.vrt.be/mig/viaa/api" xsi:schemaLocation="urn:ebu:metadata-schema:ebucore https://www.ebu.ch/metadata/schemas/EBUCore/20171009/ebucore.xsd" version="1.1">
    <xsl:output method="xml" encoding="UTF-8" indent="yes" />
    <!-- params -->
    <xsl:param name="ie_uuid" />
    <!-- vars -->
    <xsl:variable name="title" select="/VIAA/dc_title" />
    <xsl:variable name="titles_first" select="/VIAA/dc_titles/*[1]" />
    <xsl:variable name="description_short" select="/VIAA/dc_description_short" />

    <xsl:template match="VIAA">
        <metadata>
            <xsl:call-template name="title" />
            <xsl:call-template name="ie_uuid" />
            <xsl:apply-templates select="*" />
        </metadata>
    </xsl:template>

    <!-- linking identifier -->
    <xsl:template name="ie_uuid">
        <xsl:if test="$ie_uuid !=''">
            <xsl:element name="dcterms:identifier">
                <xsl:value-of select="$ie_uuid" />
            </xsl:element>
        </xsl:if>
    </xsl:template>
    <!-- Contributors -->
    <xsl:template match="dc_contributors/Aanwezig">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>aanwezig</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Adviseur">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>adviseur</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Afwezig">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>afwezig</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Archivaris">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>archivaris</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Arrangeur">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>arrangeur</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/ArtistiekDirecteur">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>artistiek_directeur</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Assistent">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>assistent</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Auteur">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>auteur</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Belichting">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>belichting</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Bijdrager">
        <xsl:element name="dcterms:contributor">
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Cameraman">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>cameraman</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Co-producer">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>coproducer</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Commentator">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>commentator</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Componist">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>componist</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/DecorOntwerper">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>decorontwerper</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Digitaliseringspartner">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>digitaliseringspartner</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Dirigent">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>dirigent</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Dramaturg">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>dramaturg</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Fotografie">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>fotografie</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Geluid">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>geluid</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Geluidsman">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>geluidsman</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/GrafischOntwerper">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>grafisch_ontwerper</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/KostuumOntwerper">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>kostuumontwerper</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Kunstenaar">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>kunstenaar</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Make-up">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>make-up</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Muzikant">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>muzikant</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Nieuwsanker">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>nieuwsanker</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Omroeper">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>omroeper</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Onderzoeker">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>onderzoeker</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Post-productie">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>postproductie</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Producer">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>producer</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Reporter">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>reporter</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Scenarist">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>scenarist</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Soundtrack">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>soundtrack</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Sponsor">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>sponsor</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/TechnischAdviseur">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>technisch_adviseur</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Uitvoerder">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>uitvoerder</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Verontschuldigd">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>verontschuldigd</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Vertaler">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>vertaler</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Verteller">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>verteller</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_contributors/Voorzitter">
        <xsl:element name="dcterms:contributor">
            <xsl:attribute name="schema:roleName">
                <xsl:text>voorzitter</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Coverages (spatial) -->
    <xsl:template match="dc_coverages/ruimte">
        <xsl:element name="dcterms:spatial">
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Coverages (temporal) -->
    <xsl:template match="dc_coverages/tijd">
        <xsl:element name="dcterms:temporal">
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Creators -->
    <xsl:template match="dc_creators/Acteur">
        <xsl:element name="dcterms:creator">
            <xsl:attribute name="schema:roleName">
                <xsl:text>acteur</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_creators/Archiefvormer">
        <xsl:element name="dcterms:creator">
            <xsl:attribute name="schema:roleName">
                <xsl:text>archiefvormer</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_creators/Auteur">
        <xsl:element name="dcterms:creator">
            <xsl:attribute name="schema:roleName">
                <xsl:text>auteur</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_creators/Cast">
        <xsl:element name="dcterms:creator">
            <xsl:attribute name="schema:roleName">
                <xsl:text>cast</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_creators/Choreograaf">
        <xsl:element name="dcterms:creator">
            <xsl:attribute name="schema:roleName">
                <xsl:text>choreograaf</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_creators/Cineast">
        <xsl:element name="dcterms:creator">
            <xsl:attribute name="schema:roleName">
                <xsl:text>cineast</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_creators/Componist">
        <xsl:element name="dcterms:creator">
            <xsl:attribute name="schema:roleName">
                <xsl:text>componist</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_creators/Danser">
        <xsl:element name="dcterms:creator">
            <xsl:attribute name="schema:roleName">
                <xsl:text>danser</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_creators/Documentairemaker">
        <xsl:element name="dcterms:creator">
            <xsl:attribute name="schema:roleName">
                <xsl:text>documentairemaker</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_creators/Fotograaf">
        <xsl:element name="dcterms:creator">
            <xsl:attribute name="schema:roleName">
                <xsl:text>fotograaf</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_creators/Interviewer">
        <xsl:element name="dcterms:creator">
            <xsl:attribute name="schema:roleName">
                <xsl:text>interviewer</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_creators/Kunstenaar">
        <xsl:element name="dcterms:creator">
            <xsl:attribute name="schema:roleName">
                <xsl:text>kunstenaar</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_creators/Maker">
        <xsl:element name="dcterms:creator">
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_creators/Muzikant">
        <xsl:element name="dcterms:creator">
            <xsl:attribute name="schema:roleName">
                <xsl:text>muzikant</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_creators/Opdrachtgever">
        <xsl:element name="dcterms:creator">
            <xsl:attribute name="schema:roleName">
                <xsl:text>opdrachtgever</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_creators/Performer">
        <xsl:element name="dcterms:creator">
            <xsl:attribute name="schema:roleName">
                <xsl:text>performer</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_creators/Producer">
        <xsl:element name="dcterms:creator">
            <xsl:attribute name="schema:roleName">
                <xsl:text>producer</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_creators/Productiehuis">
        <xsl:element name="dcterms:creator">
            <xsl:attribute name="schema:roleName">
                <xsl:text>productiehuis</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_creators/Regisseur">
        <xsl:element name="dcterms:creator">
            <xsl:attribute name="schema:roleName">
                <xsl:text>regisseur</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_creators/Schrijver">
        <xsl:element name="dcterms:creator">
            <xsl:attribute name="schema:roleName">
                <xsl:text>schrijver</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_creators/Geïnterviewde">
        <xsl:element name="dcterms:creator">
            <xsl:attribute name="schema:roleName">
                <xsl:text>geïnterviewde</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Description -->
    <xsl:template match="dc_description">
        <xsl:element name="dcterms:description">
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Description language-->
    <xsl:template match="dc_description_lang">
        <xsl:element name="dcterms:abstract">
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Description subtitles-->
    <xsl:template match="dc_description_ondertitels">
        <xsl:element name="schema:caption">
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Description transcription-->
    <xsl:template match="dc_description_transcriptie">
        <xsl:element name="schema:transcript">
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Languages-->
    <xsl:template match="dc_languages/multiselect">
        <xsl:element name="dcterms:language">
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Publisher distributor-->
    <xsl:template match="dc_publishers/Distributeur">
        <xsl:element name="dcterms:publisher">
            <xsl:attribute name="schema:roleName">
                <xsl:text>distributeur</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Publisher exposer-->
    <xsl:template match="dc_publishers/Exposant">
        <xsl:element name="dcterms:publisher">
            <xsl:attribute name="schema:roleName">
                <xsl:text>exposant</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Publisher press agency-->
    <xsl:template match="dc_publishers/Persagentschap">
        <xsl:element name="dcterms:publisher">
            <xsl:attribute name="schema:roleName">
                <xsl:text>persagentschap</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Publisher-->
    <xsl:template match="dc_publishers/Publisher">
        <xsl:element name="dcterms:publisher">
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Relations has part-->
    <xsl:template match="dc_relations/bevat">
        <xsl:element name="dcterms:hasPart">
            <xsl:attribute name="xsi:type">
                <xsl:text>premis:intellectualEntity</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Relations is part of-->
    <xsl:template match="dc_relations/is_deel_van">
        <xsl:element name="dcterms:isPartOf">
            <xsl:attribute name="xsi:type">
                <xsl:text>premis:intellectualEntity</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Relations is related to-->
    <xsl:template match="dc_relations/is_verwant_aan">
        <xsl:element name="dcterms:relation">
            <xsl:attribute name="xsi:type">
                <xsl:text>premis:intellectualEntity</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Rights comment-->
    <xsl:template match="dc_rights_comment">
        <xsl:element name="dcterms:rights">
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Rights credit-->
    <xsl:template match="dc_rights_credit">
        <xsl:element name="schema:creditText">
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Rights licenses -->
    <xsl:template match="dc_rights_licenses/multiselect">
        <xsl:element name="dcterms:license">
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Rights owner author -->
    <xsl:template match="dc_rights_rightsOwners/Auteursrechthouder">
        <xsl:element name="dcterms:rightsHolder">
            <xsl:attribute name="schema:roleName">
                <xsl:text>auteursrechthouder</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Rights holder license-->
    <xsl:template match="dc_rights_rightsHolders/Licentiehouder">
        <xsl:element name="dcterms:rightsHolder">
            <xsl:attribute name="schema:roleName">
                <xsl:text>licentiehouder</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Subjects -->
    <xsl:template match="dc_subjects/Trefwoord | dc_Subjects/Trefwoord">
        <xsl:element name="dcterms:subject">
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Titles episode -->
    <xsl:template match="dc_titles/aflevering | dc_titles/episode">
        <xsl:element name="dcterms:isPartOf">
            <xsl:attribute name="xsi:type">
                <xsl:text>schema:Episode</xsl:text>
            </xsl:attribute>
            <xsl:element name="dcterms:title">
                <xsl:value-of select="text()" />
            </xsl:element>
        </xsl:element>
    </xsl:template>

    <!-- Titles programma-->
    <xsl:template match="dc_titles/programma">
        <xsl:element name="dcterms:isPartOf">
            <xsl:attribute name="xsi:type">
                <xsl:text>schema:BroadcastEvent</xsl:text>
            </xsl:attribute>
            <xsl:element name="dcterms:title">
                <xsl:value-of select="text()" />
            </xsl:element>
            <xsl:if test="../../dc_description_programme">
                <xsl:element name="dcterms:description">
                    <xsl:value-of select="../../dc_description_programme" />
                </xsl:element>
            </xsl:if>
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_description_programme">
        <xsl:if test="not(../dc_titles/programma)">
            <xsl:element name="dcterms:isPartOf">
                <xsl:attribute name="xsi:type">
                    <xsl:text>schema:BroadcastEvent</xsl:text>
                </xsl:attribute>
                <xsl:element name="dcterms:description">
                    <xsl:value-of select="text()" />
                </xsl:element>
            </xsl:element>
        </xsl:if>
    </xsl:template>

    <!-- Titles alternative -->
    <xsl:template match="dc_titles/alternatief">
        <xsl:element name="dcterms:alternative">
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Titles (partial)archive -->
    <xsl:template match="dc_titles/archief">
        <xsl:element name="dcterms:isPartOf">
            <xsl:attribute name="xsi:type">
                <xsl:text>schema:ArchiveComponent</xsl:text>
            </xsl:attribute>
            <xsl:element name="dcterms:title">
                <xsl:value-of select="text()" />
            </xsl:element>
            <xsl:if test="../deelarchief">
                <xsl:element name="dcterms:hasPart">
                    <xsl:attribute name="xsi:type">
                        <xsl:text>schema:ArchiveComponent</xsl:text>
                    </xsl:attribute>
                    <xsl:element name="dcterms:title">
                        <xsl:value-of select="../deelarchief" />
                    </xsl:element>
                </xsl:element>
            </xsl:if>
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_titles/deelarchief">
        <xsl:if test="not(../archief)">
            <xsl:element name="dcterms:isPartOf">
                <xsl:attribute name="xsi:type">
                    <xsl:text>schema:ArchiveComponent</xsl:text>
                </xsl:attribute>
                <xsl:element name="dcterms:hasPart">
                    <xsl:attribute name="xsi:type">
                        <xsl:text>schema:ArchiveComponent</xsl:text>
                    </xsl:attribute>
                    <xsl:element name="dcterms:title">
                        <xsl:value-of select="text()" />
                    </xsl:element>
                </xsl:element>
            </xsl:element>
        </xsl:if>
    </xsl:template>

    <!-- Titles (partial)series -->
    <xsl:template match="dc_titles/reeks | dc_titles/serie">
        <xsl:element name="dcterms:isPartOf">
            <xsl:attribute name="xsi:type">
                <xsl:text>schema:CreativeWorkSeries</xsl:text>
            </xsl:attribute>
            <xsl:element name="dcterms:title">
                <xsl:value-of select="text()" />
            </xsl:element>
            <xsl:if test="../serienummer">
                <xsl:element name="dcterms:identifier">
                    <xsl:value-of select="../serienummer" />
                </xsl:element>
            </xsl:if>
            <xsl:if test="../deelreeks">
                <xsl:element name="dcterms:hasPart">
                    <xsl:attribute name="xsi:type">
                        <xsl:text>schema:CreativeWorkSeries</xsl:text>
                    </xsl:attribute>
                    <xsl:element name="dcterms:title">
                        <xsl:value-of select="../deelreeks" />
                    </xsl:element>
                </xsl:element>
            </xsl:if>
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_titles/deelreeks">
        <xsl:if test="not(../reeks or ../serie)">
            <xsl:element name="dcterms:isPartOf">
                <xsl:attribute name="xsi:type">
                    <xsl:text>schema:CreativeWorkSeries</xsl:text>
                </xsl:attribute>
                <xsl:if test="../serienummer">
                    <xsl:element name="dcterms:identifier">
                        <xsl:value-of select="../serienummer" />
                    </xsl:element>
                </xsl:if>
                <xsl:element name="dcterms:hasPart">
                    <xsl:attribute name="xsi:type">
                        <xsl:text>schema:CreativeWorkSeries</xsl:text>
                    </xsl:attribute>
                    <xsl:element name="dcterms:title">
                        <xsl:value-of select="text()" />
                    </xsl:element>
                </xsl:element>
            </xsl:element>
        </xsl:if>
    </xsl:template>

    <xsl:template match="dc_titles/serienummer">
        <xsl:if test="not(../reeks or ../serie or ../deelreeks)">
            <xsl:element name="dcterms:isPartOf">
                <xsl:attribute name="xsi:type">
                    <xsl:text>schema:CreativeWorkSeries</xsl:text>
                </xsl:attribute>
                <xsl:element name="dcterms:identifier">
                    <xsl:value-of select="text()" />
                </xsl:element>
            </xsl:element>
        </xsl:if>
    </xsl:template>


    <!-- Titles registration -->
    <xsl:template match="dc_titles/registratie">
        <xsl:element name="dcterms:title">
            <xsl:attribute name="xsi:type">
                <xsl:text>meemoo:RegistrationTitle</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Titles season -->
    <xsl:template match="dc_titles/seizoen">
        <xsl:element name="dcterms:isPartOf">
            <xsl:attribute name="xsi:type">
                <xsl:text>schema:CreativeWorkSeason</xsl:text>
            </xsl:attribute>
            <xsl:element name="dcterms:title">
                <xsl:value-of select="text()" />
            </xsl:element>
            <xsl:if test="../seizoennummer">
                <xsl:element name="schema:seasonNumber">
                    <xsl:value-of select="../seizoennummer" />
                </xsl:element>
            </xsl:if>
        </xsl:element>
    </xsl:template>

    <xsl:template match="dc_titles/seizoennummer">
        <xsl:if test="not(../seizoen)">
            <xsl:element name="dcterms:isPartOf">
                <xsl:attribute name="xsi:type">
                    <xsl:text>schema:CreativeWorkSeason</xsl:text>
                </xsl:attribute>
                <xsl:element name="schema:seasonNumber">
                    <xsl:value-of select="text()" />
                </xsl:element>
            </xsl:element>
        </xsl:if>
    </xsl:template>

    <!-- Types -->
    <xsl:template match="dc_types/multiselect">
        <xsl:element name="schema:genre">
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Created -->
    <xsl:template match="dcterms_created">
        <xsl:element name="dcterms:created">
            <xsl:attribute name="xsi:type">
                <xsl:text>EDTF-level1</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Issued -->
    <xsl:template match="dcterms_issued">
        <xsl:element name="dcterms:issued">
            <xsl:attribute name="xsi:type">
                <xsl:text>EDTF-level1</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <!-- Title

    In order:
     - dc_title
     - dc_titles/*[1] - first element in dc_titles
     - dc_short_description
    -->
    <xsl:template name="title">
        <xsl:if test="$title !=''">
            <xsl:element name="dcterms:title">
                <xsl:value-of select="$title" />
            </xsl:element>
        </xsl:if>
        <xsl:if test="$titles_first !='' and not($title != '')">
            <xsl:element name="dcterms:title">
                <xsl:value-of select="$titles_first" />
            </xsl:element>
        </xsl:if>
        <xsl:if test="$description_short !='' and not($titles_first !='' or $title !='')">
            <xsl:element name="dcterms:title">
                <xsl:value-of select="$description_short" />
            </xsl:element>
        </xsl:if>
    </xsl:template>

    <!-- EBU Object Type-->
    <xsl:template match="ebu_objectType">
        <xsl:element name="ebucore:type">
            <xsl:value-of select="text()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="@*|node()">
        <xsl:apply-templates select="node()" />
    </xsl:template>
</xsl:stylesheet>