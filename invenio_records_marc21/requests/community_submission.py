# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Community submission request."""


from invenio_drafts_resources.services.records.uow import ParentRecordCommitOp
from invenio_notifications.services.uow import NotificationOp
from invenio_rdm_records.notifications.builders import (
    CommunityInclusionAcceptNotificationBuilder,
)
from invenio_rdm_records.requests import CommunitySubmission
from invenio_rdm_records.requests.community_submission import (
    CancelAction,
    DeclineAction,
    ExpireAction,
)
from invenio_requests.customizations import actions

from ..proxies import current_records_marc21 as service


#
# Actions
#
class SubmitAction(actions.SubmitAction):
    """Submit action."""

    def execute(self, identity, uow):
        """Execute the submit action."""
        draft = self.request.topic.resolve()
        service.records_service._validate_draft(identity, draft)
        # Set the record's title as the request title.
        fields = draft.metadata.get("fields", None)
        self.request["title"] = (
            str(fields.get("245", "No Title")) if fields is not None else "NO Title"
        )
        super().execute(identity, uow)


class AcceptAction(actions.AcceptAction):
    """Accept action."""

    def execute(self, identity, uow):
        """Accept record into community."""
        # Resolve the topic and community - the request type only allow for
        # community receivers and record topics.
        draft = self.request.topic.resolve()
        community = self.request.receiver.resolve()
        # service._validate_draft(identity, draft) # todo

        # validate record and community access
        # todo
        # if not is_access_restriction_valid(draft, community):
        #     raise InvalidAccessRestrictions()

        # Unset review from record (still accessible from request)
        # The curator (receiver) should still have access, via the community
        # The creator (uploader) should also still have access, because
        # they're the uploader

        draft.parent.review = None

        # TODO:
        # - Put below into a service method
        # - Check permissions

        # Add community to record.
        is_default = self.request.type.set_as_default
        draft.parent.communities.add(
            community, request=self.request, default=is_default
        )

        if getattr(community, "parent", None):
            draft.parent.communities.add(community.parent, request=self.request)

        # todo
        uow.register(
            ParentRecordCommitOp(
                draft.parent, indexer_context=dict(service=service.records_service)
            )
        )
        print(f"AcceptAction.execute draft: {draft}, parent: {draft.parent}")
        # Publish the record
        # TODO: Ensure that the accepting user has permissions to publish.
        service.records_service.publish(identity, draft.pid.pid_value, uow=uow)
        uow.register(
            NotificationOp(
                CommunityInclusionAcceptNotificationBuilder.build(
                    identity=identity, request=self.request
                )
            )
        )
        super().execute(identity, uow)


#
# Request
#
class Marc21CommunitySubmission(CommunitySubmission):
    """Review request for submitting a record to a community."""

    type_id = "marc21-community-submission"
    allowed_topic_ref_types = ["marcrecord"]

    available_actions = {
        "create": actions.CreateAction,
        "submit": SubmitAction,
        "delete": actions.DeleteAction,
        "accept": AcceptAction,
        "decline": DeclineAction,
        "cancel": CancelAction,
        "expire": ExpireAction,
    }
