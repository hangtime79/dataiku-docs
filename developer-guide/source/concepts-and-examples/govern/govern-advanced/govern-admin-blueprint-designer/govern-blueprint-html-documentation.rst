Govern Blueprint HTML Documentation
###################################

In each view component, you have the possibility to define a HTML documentation which will be displayed along with the component itself.

Example 1. Create a show more/less button
=========================================

In the case of a very long content in the HTML documentation of a view component, it may be useful to have a "show more" / "show less" button to be able to hide / show part of this content.

Note that you need to make sure that the IDs of the tag elements in the code are unique among all documentations shown in a page. You may want to generate a unique identifier as a prefix for all the IDs for this purpose.

The following HTML can be used in a HTML documentation field in the Blueprint Designer to add a "show more" / "show less" button:

.. code-block:: html

    A program initiative is a coordinated set of activities, projects, or strategic efforts designed to achieve specific long-term business objectives.
	<br><br>

	<button id="0250de15a30e-showmore-button" onclick="document.getElementById('0250de15a30e-text').style['display'] = 'inherit';document.getElementById('0250de15a30e-showless-button').style['display'] = 'inherit';document.getElementById('0250de15a30e-showmore-button').style['display'] = 'none';">Show more</button>

	<button id="0250de15a30e-showless-button" onclick="document.getElementById('0250de15a30e-text').style['display'] = 'none';document.getElementById('0250de15a30e-showmore-button').style['display'] = 'inherit';document.getElementById('0250de15a30e-showless-button').style['display'] = 'none';" style="display: none;">Show less</button>

	<div id="0250de15a30e-text" style="display:none">
	<br>
	These initiatives are typically aligned with the organization's broader mission and vision, aiming to drive significant growth, innovation, or transformation across various departments or functions.
	<br><br>
	Key Characteristics of a Program Initiative:
	<br><br>
	1 - Strategic Alignment: Program initiatives are directly linked to the company’s strategic goals. They are often part of a larger portfolio of initiatives that collectively support the company's long-term vision, such as entering new markets, enhancing operational efficiency, or launching new products.
	<br><br>
	2 - Cross-Functional Collaboration: These initiatives usually require the collaboration of multiple departments or business units. For instance, a program focused on digital transformation might involve IT, operations, marketing, and human resources working together to modernize the company’s technology infrastructure and processes.
	<br><br>
	3 - Resource Allocation: Due to their complexity and scope, program initiatives typically require substantial resources, including budget, personnel, and time. They are often managed by a dedicated program manager or team, responsible for overseeing the initiative’s progress and ensuring it stays on track.
	<br><br>
	4 - Long-Term Focus: Unlike short-term projects, program initiatives are long-term efforts that may span several months or even years. They are designed to create lasting impact, such as implementing a company-wide sustainability strategy or overhauling a customer relationship management (CRM) system.
	<br><br>
	5 - Measurable Outcomes: Success for a program initiative is measured against clearly defined outcomes or key performance indicators (KPIs). These might include financial metrics, such as revenue growth, or operational metrics, like improved customer satisfaction or reduced time-to-market.
	<br><br>
	6 - Governance and Oversight: Program initiatives typically involve a formal governance structure to monitor progress, manage risks, and ensure alignment with the company’s overall strategy. This might include regular reporting to senior leadership and adjustments to the initiative’s scope or direction as needed.
	</div>


